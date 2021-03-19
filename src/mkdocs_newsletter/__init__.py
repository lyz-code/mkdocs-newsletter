"""Automatically create newsletters from the changes in a mkdocs repository."""

from typing import List

from .entrypoints.mkdocs_plugin import Newsletter
from .model import Change
from .services.git import semantic_changes
from .services.newsletter import digital_garden_changes, last_newsletter_changes

__all__: List[str] = [
    "Change",
    "semantic_changes",
    "digital_garden_changes",
    "last_newsletter_changes",
    "Newsletter",
]
