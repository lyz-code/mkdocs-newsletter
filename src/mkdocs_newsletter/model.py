"""Module to store the common business model of all entities."""

import os
import re
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import List, Optional

from dateutil import tz
from pydantic import BaseModel, Field, HttpUrl


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


class NewsletterType(str, Enum):
    """Defines the possible newsletter types."""

    YEARLY = "yearly"
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    DAILY = "daily"


class Newsletter(BaseModel):
    """Represents a newsletter."""

    file_: Path

    @property
    def basename(self) -> str:
        """Return the basename of the Newsletter."""
        return os.path.splitext(self.file_.name)[0]

    @property
    def type_(self) -> str:
        """Return the type of the Newsletter."""
        if re.match(r"\d{4}$", self.basename):
            return "yearly"
        if re.match(r"\d{4}_\d{2}$", self.basename):
            return "monthly"
        if re.match(r"\d{4}_w\d{2}$", self.basename):
            return "weekly"
        if re.match(r"\d{4}_\d{2}_\d{2}$", self.basename):
            return "daily"
        raise ValueError("Can't extract type from file path")

    @property
    def date(self) -> datetime:
        """Return the date of the Newsletter."""
        if re.match(r"\d{4}$", self.basename):
            return datetime(int(self.basename), 1, 1, tzinfo=tz.tzlocal())
        if re.match(r"\d{4}_\d{2}$", self.basename):
            year = int(self.basename.split("_")[0])
            month = int(self.basename.split("_")[1])
            return datetime(year, month, 1, tzinfo=tz.tzlocal())
        if re.match(r"\d{4}_w\d{2}$", self.basename):
            year = int(self.basename.split("_")[0])
            week = int(self.basename.split("w")[1])
            first_day = datetime(year, 1, 1, tzinfo=tz.tzlocal())
            return first_day + timedelta(days=7 * (week - 1) - first_day.weekday())
        if re.match(r"\d{4}_\d{2}_\d{2}$", self.basename):
            return datetime.strptime(self.basename, "%Y_%m_%d").replace(
                tzinfo=tz.tzlocal()
            )
        raise ValueError("Can't extract date from file path")

    def __lt__(self, other: "Newsletter") -> bool:
        """Assert if an object is smaller than us.

        Args:
            other: Newsletter to compare.

        Raises:
            TypeError: If the id type of the objects is not compatible.
        """
        return self.basename < other.basename

    def __gt__(self, other: "Newsletter") -> bool:
        """Assert if an object is greater than us.

        Args:
            other: Newsletter to compare.

        Raises:
            TypeError: If the id type of the objects is not compatible.
        """
        return self.basename > other.basename


class Newsletters(BaseModel):
    """Represents the newsletters for each feed type."""

    yearly: List[Newsletter] = Field(default_factory=list)
    monthly: List[Newsletter] = Field(default_factory=list)
    weekly: List[Newsletter] = Field(default_factory=list)
    daily: List[Newsletter] = Field(default_factory=list)

    def sort(self) -> None:
        """Sort the newsletters."""
        self.yearly = sorted(self.yearly, reverse=True)
        self.monthly = sorted(self.monthly, reverse=True)
        self.weekly = sorted(self.weekly, reverse=True)
        self.daily = sorted(self.daily, reverse=True)


class LastNewsletter(BaseModel):
    """Represents the last newsletter for each feed type."""

    yearly: Optional[datetime] = None
    monthly: Optional[datetime] = None
    weekly: Optional[datetime] = None
    daily: Optional[datetime] = None

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


class FeedEntry(BaseModel):
    """Model an RSS feed entry."""

    title: str
    link: HttpUrl
    published: datetime
    description: str
    author: Optional[str]
    image: None = None

    def __lt__(self, other: "FeedEntry") -> bool:
        """Assert if an object is smaller than us.

        Args:
            other: FeedEntry to compare.

        Raises:
            TypeError: If the id type of the objects is not compatible.
        """
        return self.published < other.published

    def __gt__(self, other: "FeedEntry") -> bool:
        """Assert if an object is greater than us.

        Args:
            other: FeedEntry to compare.

        Raises:
            TypeError: If the id type of the objects is not compatible.
        """
        return self.published > other.published


class Feed(BaseModel):
    """Model an RSS feed."""

    ttl: int
    generator: str
    title: Optional[str]
    link: Optional[HttpUrl]
    rss_link: Optional[HttpUrl]
    published: Optional[datetime]
    logo: Optional[HttpUrl]
    description: Optional[str]
    author: Optional[str]
    entries: List[FeedEntry] = Field(default_factory=list)


Newsletter.update_forward_refs()
NewsletterSection.update_forward_refs()
FeedEntry.update_forward_refs()
