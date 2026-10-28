import re
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from contentctl.objects.deployment_email import DeploymentEmail
from contentctl.output.conf_writer import ConfWriter

TEMPLATE = (
    Path(__file__).parent.parent
    / "contentctl"
    / "output"
    / "templates"
    / "savedsearches_detections.j2"
)
REQUIRED = {"to": "sim@example.com", "subject": "Splunk: $name$", "message": "$name$"}


def render_email_block(email: DeploymentEmail) -> list[str]:
    # Render only the email block of the real template, since rendering the whole
    # template requires a fully populated Detection
    match = re.search(
        r"{% if detection\.deployment\.alert_action\.email %}.*?{% endif %}\n",
        TEMPLATE.read_text(),
        re.DOTALL,
    )
    assert match is not None
    detection = SimpleNamespace(
        name="Test Detection",
        deployment=SimpleNamespace(alert_action=SimpleNamespace(email=email)),
    )
    template = ConfWriter.getJ2Environment().from_string(match.group(0))
    return template.render(detection=detection).splitlines()


def test_defaults_send_results_inline_as_table():
    lines = render_email_block(DeploymentEmail(**REQUIRED))
    for expected in [
        "action.email = 1",
        "action.email.sendresults = 1",
        "action.email.inline = 1",
        "action.email.format = csv",
        "action.email.sendcsv = 0",
        "action.email.maxresults = 50",
    ]:
        assert expected in lines


def test_overrides_are_rendered():
    email = DeploymentEmail(
        **REQUIRED,
        sendresults=False,
        inline=False,
        format="csv",
        sendcsv=True,
        maxresults=10,
    )
    lines = render_email_block(email)
    for expected in [
        "action.email.sendresults = 0",
        "action.email.inline = 0",
        "action.email.format = csv",
        "action.email.sendcsv = 1",
        "action.email.maxresults = 10",
    ]:
        assert expected in lines


@pytest.mark.parametrize(
    "override",
    [{"format": "html"}, {"maxresults": 0}, {"unknown_field": True}],
)
def test_invalid_values_are_rejected(override):
    with pytest.raises(ValidationError):
        DeploymentEmail(**REQUIRED, **override)
