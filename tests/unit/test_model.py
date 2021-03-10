"""Test the models."""

from datetime import datetime

from dateutil import tz

from mkdocs_newsletter.model import LastNewsletter


def test_last_newsletter_min_returns_the_smallest_date() -> None:
    """
    Given: A LastNewsletter object with different dates.
    When: min is called
    Then: The smallest one is returned
    """
    last_changes = LastNewsletter(
        year=datetime(2020, 1, 1, tzinfo=tz.tzlocal()),
        week=datetime(2020, 2, 2, tzinfo=tz.tzlocal()),
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
