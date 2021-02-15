"""Automatically create newsletters from the changes in a mkdocs repository."""

from typing import List

from . import services
from .model import Change

__all__: List[str] = ["Change", "services"]
