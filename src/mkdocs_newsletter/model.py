"""Module to store the common business model of all entities."""

from datetime import datetime
from typing import List, Optional

from pydantic import Field
from pydantic.main import BaseModel


class Change(BaseModel):
    """Represent a single semantic change in a git repository.

    Attributes:
        date: When the change was done.
        summary: short description of the change.
        type_: semantic type of change, such as feature or fix.
        message: long description of the change.
        breaking: if the change breaks previous functionality.
        category: name of the group of files that share meaning.
        category_order: order of the category against all categories.
        subcategory: name of the subgroup of files that share meaning.
        category_order: order of the subcategory against all subcategories.
        file_: markdown file name.
        file_section: title of the file containing the change.
        file_section_order: order of the file in the subcategory or category that holds
            the file.
        file_subsection: title of the section of the file the change belongs to.
    """

    date: datetime
    summary: str
    scope: Optional[str]
    type_: Optional[str]
    message: Optional[str] = None
    breaking: bool = False
    publish: Optional[bool] = None
    category: Optional[str] = None
    category_order: Optional[int] = None
    subcategory: Optional[str] = None
    subcategory_order: Optional[int] = None
    file_: Optional[str] = None
    file_section: Optional[str] = None
    file_section_order: Optional[int] = None
    file_subsection: Optional[str] = None


class DigitalGardenChanges(BaseModel):
    """Represents all changes that need to be published for each feed type."""

    daily: List[Change] = Field(default_factory=list)
    weekly: List[Change] = Field(default_factory=list)
    monthly: List[Change] = Field(default_factory=list)
    yearly: List[Change] = Field(default_factory=list)


class LastNewsletter(BaseModel):
    """Represents the last newsletter for each feed type."""

    year: Optional[datetime] = None
    month: Optional[datetime] = None
    week: Optional[datetime] = None
    day: Optional[datetime] = None

    def min(self) -> Optional[datetime]:
        """Return the smallest date of all the feeds."""
        try:
            return min(value for key, value in self.dict().items() if value is not None)
        except ValueError:
            return None


class NewsletterSection(BaseModel):
    """Represent the section of a newsletter article.

    Attributes:
        title: Category title
        order: The order in comparison with the other categories
        changes: Changes to be printed in the section
        subsections: A list of subsections.
    """

    title: str
    order: int
    url: Optional[str] = None
    changes: List[Change] = Field(default_factory=list)
    subsections: List["NewsletterSection"] = Field(default_factory=list)

    def __lt__(self, other: "NewsletterSection") -> bool:
        """Assert if an object is smaller than us.

        Args:
            other: NewsletterSection to compare.

        Raises:
            TypeError: If the id type of the objects is not compatible.
        """
        return self.order > other.order

    def __gt__(self, other: "NewsletterSection") -> bool:
        """Assert if an object is greater than us.

        Args:
            other: NewsletterSection to compare.

        Raises:
            TypeError: If the id type of the objects is not compatible.
        """
        return self.order < other.order


NewsletterSection.update_forward_refs()
