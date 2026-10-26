from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DeploymentEmail(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str
    subject: str
    to: str
    # Results are sent inline as plain text in the email body by default, rather
    # than as a CSV attachment. Each detection may override these.
    sendresults: bool = True
    inline: bool = True
    format: Literal["table", "raw", "csv", "plain"] = "plain"
    sendcsv: bool = False
    maxresults: int = Field(default=50, ge=1)
