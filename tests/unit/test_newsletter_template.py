"""Test the newsletter article template."""

from datetime import datetime
from textwrap import dedent

from dateutil import tz

from mkdocs_newsletter.model import Change
from mkdocs_newsletter.services.newsletter import create_newsletter


def test_newsletter_prints_level_1_change() -> None:
    """
    Given: a change that affects a level 1 article.
    When: create_newsletter is called
    Then: The category of the article is added as title 1 and the change as a
        bullet point.
    """
    changes = [
        Change(
            date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
            summary="Add introduction",
            type_="feature",
            file_="index.md",
            category="Introduction",
            category_order=0,
        ),
    ]

    result = create_newsletter(changes)

    assert result == dedent(
        """\
        # [Introduction](index.md)

        * New: Add introduction"""
    )


def test_newsletter_prints_level_2_change() -> None:
    """
    Given: a change that affects a level 2 article.
    When: create_newsletter is called
    Then: The category of the article is added as title 2 and the change as a
        bullet point.
    """
    changes = [
        Change(
            date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
            summary="Add trees",
            type_="feature",
            file_="trees.md",
            category="Botany",
            category_order=0,
            subcategory="Trees",
            subcategory_order=0,
        ),
    ]

    result = create_newsletter(changes)

    assert result == dedent(
        """\
        # Botany

        ## [Trees](trees.md)

        * New: Add trees"""
    )


def test_newsletter_prints_level_3_change() -> None:
    """
    Given: a change that affects a level 3 article.
    When: create_newsletter is called
    Then: The category of the article is added as title 3 and the change as a
        bullet point.
    """
    changes = [
        Change(
            date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
            summary="Add helm",
            type_="feature",
            file_="helm.md",
            category="DevOps",
            category_order=0,
            subcategory="Infrastructure as Code",
            subcategory_order=0,
            file_section="Helm",
            file_section_order=0,
        ),
    ]

    result = create_newsletter(changes)

    assert result == dedent(
        """\
        # DevOps

        ## Infrastructure as Code

        ### [Helm](helm.md)

        * New: Add helm"""
    )


def test_template_prints_changes_in_chronological_order() -> None:
    """
    Given: two changes that affects a level 1 article.
    When: create_newsletter is called
    Then: The category of the article is added as title 1 and the changes ordered by
        date as bullet points.
    """
    changes = [
        Change(
            date=datetime(2021, 2, 9, tzinfo=tz.tzlocal()),
            summary="Add new content",
            type_="performance",
            file_="index.md",
            category="Introduction",
            category_order=0,
        ),
        Change(
            date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
            summary="Add introduction",
            type_="feature",
            file_="index.md",
            category="Introduction",
            category_order=0,
        ),
    ]

    result = create_newsletter(changes)

    assert result == dedent(
        """\
        # [Introduction](index.md)

        * New: Add introduction
        * Improvement: Add new content"""
    )


def test_template_prints_changes_with_subsection_link() -> None:
    """
    Given: a changes that affects a level 1 article with the subsection information.
    When: create_newsletter is called
    Then: The category of the article is added as title 1 with a link to the subsection
    """
    changes = [
        Change(
            date=datetime(2021, 2, 9, tzinfo=tz.tzlocal()),
            summary="Add new content",
            type_="performance",
            file_="index.md",
            category="Introduction",
            category_order=0,
            file_subsection="#article-subsection",
        ),
    ]

    result = create_newsletter(changes)

    assert result == dedent(
        """\
        # [Introduction](index.md)

        * Improvement: [Add new content](index.md#article-subsection)"""
    )


def test_template_prints_changes_with_message() -> None:
    """
    Given: a changes that affects a level 1 article with the message information.
    When: create_newsletter is called.
    Then: The category of the article is added as title 1 with the description and
        the commit message are separated by a new line.
    """
    changes = [
        Change(
            date=datetime(2021, 2, 9, tzinfo=tz.tzlocal()),
            summary="Add new content",
            type_="performance",
            file_="index.md",
            category="Introduction",
            category_order=0,
            message="Short change description.",
        ),
        Change(
            date=datetime(2021, 2, 9, tzinfo=tz.tzlocal()),
            summary="Add more content",
            type_="performance",
            file_="index.md",
            category="Introduction",
            category_order=0,
            message="Another short change description.",
        ),
    ]

    result = create_newsletter(changes)

    assert result == dedent(
        """\
        # [Introduction](index.md)

        * Improvement: Add new content

            Short change description.

        * Improvement: Add more content

            Another short change description."""
    )


def test_template_prints_changes_with_long_message() -> None:
    """
    Given: a changes that affects a level 1 article with a long message.
    When: create_newsletter is called.
    Then: The category of the article is added as title 1 with the description
        well indented and without external line breaks. Wrapping the message has led
        to broken links in the past.
    """
    changes = [
        Change(
            date=datetime(2021, 2, 9, tzinfo=tz.tzlocal()),
            summary="Add new content",
            type_="performance",
            file_="index.md",
            category="Introduction",
            category_order=0,
            message=(
                "Really long long long long long long long long long long long long "
                "long long long long long long long long change description."
            ),
        ),
    ]

    result = create_newsletter(changes)

    assert result == (
        "# [Introduction](index.md)\n"
        "\n"
        "* Improvement: Add new content\n"
        "\n"
        "    Really long long long long long long long long long long long long long "
        "long long long long long long long change description."
    )


def test_template_sorts_changes_without_subsection() -> None:
    """
    Given: two changes to publish that belong to the same category but one doesn't have
        subcategory.
    When: create_newsletter is called
    Then: The file is created and the changes are sorted as expected
    """
    changes = [
        Change(
            date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
            summary="Create the devops introduction page.",
            type_="feature",
            scope="devops",
            category="DevOps",
            category_order=0,
            file_="devops.md",
        ),
        Change(
            date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
            summary="Create the helm introduction page.",
            type_="feature",
            scope="helm",
            category="DevOps",
            category_order=0,
            subcategory="Helm",
            subcategory_order=0,
            file_="helm.md",
        ),
    ]

    result = create_newsletter(changes)

    assert result == dedent(
        """\
        # [DevOps](devops.md)

        * New: Create the devops introduction page.

        ## [Helm](helm.md)

        * New: Create the helm introduction page."""
    )


def test_template_group_changes_by_category() -> None:
    """
    Given: three changes to publish that belong to two different categories.
    When: create_newsletter is called
    Then: The file is created and the changes are grouped by category and ordered
        according to the nav order.
    """
    changes = [
        Change(
            date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
            summary="Create the devops introduction page.",
            type_="feature",
            scope="devops",
            category="DevOps",
            category_order=0,
            file_="devops.md",
        ),
        Change(
            date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
            summary="Create the trees introduction page.",
            type_="feature",
            scope="trees",
            category="Botany",
            category_order=1,
            subcategory="Trees",
            subcategory_order=0,
            file_="trees.md",
        ),
        Change(
            date=datetime(2021, 2, 9, tzinfo=tz.tzlocal()),
            summary="Improve the devops introduction page.",
            type_="performance",
            scope="devops",
            category="DevOps",
            category_order=0,
            file_="devops.md",
        ),
    ]

    result = create_newsletter(changes)

    assert result == dedent(
        """\
        # [DevOps](devops.md)

        * New: Create the devops introduction page.
        * Improvement: Improve the devops introduction page.

        # Botany

        ## [Trees](trees.md)

        * New: Create the trees introduction page."""
    )
