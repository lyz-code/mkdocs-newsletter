"""Test the models."""

from datetime import datetime

from dateutil import tz

from mkdocs_newsletter.model import LastNewsletter, NewsletterSection


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
    # SIM204, C0113: We don't want to simplify to important > unimportant because we
    # want to test the __lt__ method
    assert not important < unimportant  # noqa: C0113, SIM204
