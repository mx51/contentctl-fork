# contentctl-fork

mx51's fork of [splunk/contentctl](https://github.com/splunk/contentctl). Upstream no longer accepts PRs, so all changes stay in this fork.

## Changes vs upstream

| Change | Where |
|---|---|
| Detections visible in the Splunk UI (`is_visible = true`) | `contentctl/output/templates/savedsearches_detections.j2` |
| Email alert result settings (see below) | `contentctl/objects/deployment_email.py`, `savedsearches_detections.j2` |
| No date suffix on lookup filenames | `CSVLookup.app_filename` in `contentctl/objects/lookup.py` |
| Test data sent to HEC `/event` instead of `/raw` | `hec_raw_replay` in `contentctl/actions/detection_testing/infrastructures/DetectionTestingInfrastructure.py` |
| 10-minute data model acceleration wait commented out | `execute_unit_test` in `DetectionTestingInfrastructure.py` |
| Requirement for 2 drilldown searches commented out (ES-only) | `model_post_init` in `contentctl/objects/abstract_security_content_objects/detection_abstract.py` |

## DeploymentEmail

Optional fields, written to every email stanza in `savedsearches.conf`. Each detection can override them under `deployment.alert_action.email`. Booleans render as `1`/`0`. `extra="forbid"` is kept, so unknown keys fail validation.

| Field | Default | conf key |
|---|---|---|
| `sendresults` | `true` | `action.email.sendresults` |
| `inline` | `true` | `action.email.inline` |
| `format` | `csv` (`table`/`raw`/`csv`/`plain`) | `action.email.format` |
| `sendcsv` | `false` | `action.email.sendcsv` |
| `maxresults` | `50` (≥ 1) | `action.email.maxresults` |

## Versioning and releases

- Version in `pyproject.toml`: `5.6.0+mx51.N` (PEP 440 local version, so it can't clash with upstream releases).
- Tag: `v5.6.0-mx51.N`, pushed as a git tag only.
- Don't create GitHub Releases. `.github/workflows/pushToPyPiOnRelease.yml` publishes to PyPI on release.
- Downstream pins this repo by tag, so any change needs a version bump, a new tag, and a pin bump downstream.

## Tests and ruff

```sh
.venv/bin/python -m pytest tests/                           # pytest is not a dev dependency; pip install it into .venv
poetry run ruff check contentctl/                           # CI (ruff.yml) runs these two on contentctl/
poetry run ruff format --check contentctl/
```

`__version__` in `contentctl/__init__.py` is a stale `0.1.0`; `pyproject.toml` holds the real version.

## Gotchas

- A stray, git-ignored venv at `contentctl/.venv` (inside the package dir) makes `poetry build` and `pip wheel .` fail with "... is not in the subpath of ...". Either delete it or build from a clean export: `git archive HEAD | tar -x -C <dir>`.
- Work on a branch and open a PR. Check `git branch --show-current` before committing; never push to `main`.
