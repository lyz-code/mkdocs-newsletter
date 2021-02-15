"""Module to store the common business model of all entities."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Change(BaseModel):
    """Represent a single semantic change in a git repository."""

    date: datetime
    summary: str
    scope: Optional[str]
    type_: Optional[str]
    message: Optional[str] = None
    breaking: bool = False
    publish: Optional[bool] = None


class DigitalGardenChanges(BaseModel):
    """Represents all changes that need to be published for each feed type."""

    daily: List[Change] = Field(default_factory=list)
    weekly: List[Change] = Field(default_factory=list)
    monthly: List[Change] = Field(default_factory=list)
    yearly: List[Change] = Field(default_factory=list)
