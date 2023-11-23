"""Test the models."""

from datetime import datetime
from pathlib import Path

import pytest
from dateutil import tz

from mkdocs_newsletter.model import (
    FeedEntry,
    LastNewsletter,
    Newsletter,
    NewsletterSection,
)


def test_last_newsletter_min_returns_the_smallest_date() -> None:
    """
    Given: A LastNewsletter object with different dates.
    When: min is called
    Then: The smallest one is returned
    """
    last_changes = LastNewsletter(
        yearly=datetime(2020, 1, 1, tzinfo=tz.tzlocal()),
        weekly=datetime(2020, 2, 2, tzinfo=tz.tzlocal()),
    )

    result = last_changes.min()

    assert result == datetime(2020, 1, 1, tzinfo=tz.tzlocal())


def test_last_newsletter_min_returns_none_if_all_empty() -> None:
    """
    Given: A LastNewsletter object with no last dates.
    When: min is called
    Then: None is returned
    """
    last_changes = LastNewsletter()

    result = last_changes.min()

    assert result is None


# AAA01: No act block
def test_newslettersection_can_order_objects() -> None:  # noqa: AAA01
    """
    Given: Two NewsletterSection objects with different orders.
    When: They are compared
    Then: The return the expected behavior
    """
    important = NewsletterSection(title="Important section", order=0)
    unimportant = NewsletterSection(title="Unimportant section", order=1)

    assert important > unimportant
    # SIM204, C0113, C0117: We don't want to simplify to important > unimportant
    # because we want to test the __lt__ method
    assert not important < unimportant  # noqa: C0113, SIM204, C0117


# AAA01: No act block
def test_newsletter_can_order_objects() -> None:  # noqa: AAA01
    """
    Given: Two Newsletter objects with different orders.
    When: They are compared
    Then: The return the expected behavior
    """
    greater = Newsletter(file_=Path("2021_01.md"))
    smaller = Newsletter(file_=Path("2020_01.md"))

    assert greater > smaller
    # SIM204, C0113, C0117: We don't want to simplify to important > unimportant
    # because we want to test the __lt__ method
    assert not greater < smaller  # noqa: C0113, SIM204, C0117


# AAA01: No act block
def test_feedentry_can_order_objects() -> None:  # noqa: AAA01
    """
    Given: Two FeedEntry objects with different orders.
    When: They are compared
    Then: The return the expected behavior
    """
    greater = FeedEntry(
        published=datetime(2021, 1, 1),
        title="Greater",
        link="https://test.com",  # type: ignore
        description="",
    )
    smaller = FeedEntry(
        published=datetime(2020, 1, 1),
        title="Smaller",
        link="https://test.com",  # type: ignore
        description="",
    )

    assert greater > smaller
    # SIM204, C0113, C0117: We don't want to simplify to important > unimportant
    # because we want to test the __lt__ method
    assert not greater < smaller  # noqa: C0113, SIM204, C0117


@pytest.mark.parametrize(
    ("property_", "message"),
    [
        ("type_", "Can't extract type from file path"),
        ("date", "Can't extract date from file path"),
    ],
)
def test_newsletter_handles_wrong_path(property_: str, message: str) -> None:
    """
    Given: A Newsletter with a path that doesn't have a date.
    When: calling the type_ and date methods
    Then: Errors are raised
    """
    newsletter = Newsletter(file_=Path("wrong_path.md"))

    with pytest.raises(ValueError, match=message):
        getattr(newsletter, property_)
