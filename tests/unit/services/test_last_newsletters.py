"""Tests the extraction of last newsletter entries for each feed type."""

import os
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import List

import pytest
from dateutil import tz
from git import Repo
from mkdocs.config.defaults import MkDocsConfig

from mkdocs_newsletter import Change, digital_garden_changes, last_newsletter_changes
from mkdocs_newsletter.model import DigitalGardenChanges, LastNewsletter
from mkdocs_newsletter.services.newsletter import (
    add_change_categories,
    create_newsletters,
)


def create_files(file_paths: List[str], repo: Repo) -> str:
    """Create the Files object with the desired files.

    Args:
        file_paths: List of paths.

    Returns:
        The newsletter directory.
    """
    newsletter_dir = f"{repo.working_dir}/docs/newsletter"

    if not os.path.exists(newsletter_dir):
        os.makedirs(newsletter_dir)

    for file_path in file_paths:
        Path(f"{newsletter_dir}/{file_path}").touch()

    return newsletter_dir


def test_last_newsletters_extracts_last_year(repo: Repo) -> None:
    """
    Given: A Files object with two File objects newsletter/2020.md and
        newsletter/2019.md.
    When: last_newsletters is called
    Then: A LastNewsletter object is returned that returns a datetime object with
        2021-01-01 as last date for the year periodicity.
    """
    newsletter_dir = create_files(["2019.md", "2020.md"], repo)

    result = last_newsletter_changes(newsletter_dir)

    assert result.yearly == datetime(2021, 1, 1, tzinfo=tz.tzlocal())


def test_last_newsletters_extracts_last_month(repo: Repo) -> None:
    """
    Given: A Files object with two File objects newsletter/2020_01.md and
        newsletter/2020_02.md.
    When: last_newsletters is called
    Then: A LastNewsletter object is returned that returns a datetime object with
        2020-03-01 as last date for the month periodicity.
    """
    newsletter_dir = create_files(["2020_01.md", "2020_02.md"], repo)

    result = last_newsletter_changes(newsletter_dir)

    assert result.monthly == datetime(2020, 3, 1, tzinfo=tz.tzlocal())


def test_last_newsletters_extracts_last_month_of_the_year(repo: Repo) -> None:
    """
    Given: A Files object with a File object newsletter/2020_11.md and
        newsletter/2020_12.md.
    When: last_newsletters is called
    Then: A LastNewsletter object is returned that returns a datetime object with
        2021-01-01 as last date for the month periodicity.
    """
    newsletter_dir = create_files(["2020_11.md", "2020_12.md"], repo)

    result = last_newsletter_changes(newsletter_dir)

    assert result.monthly == datetime(2021, 1, 1, tzinfo=tz.tzlocal())


def test_last_newsletters_extracts_last_week(repo: Repo) -> None:
    """
    Given: A Files object with two File objects newsletter/2020_w01.md and
        newsletter/2020_w02.md.
    When: last_newsletters is called
    Then: A LastNewsletter object is returned that returns a datetime object with
        the monday of the third week of the year for the week periodicity.
    """
    newsletter_dir = create_files(["2020_w01.md", "2020_w02.md"], repo)

    result = last_newsletter_changes(newsletter_dir)

    assert result.weekly == datetime(2020, 1, 13, tzinfo=tz.tzlocal())


def test_last_newsletters_extracts_last_day(repo: Repo) -> None:
    """
    Given: A Files object with two File objects newsletter/2020_01_01.md and
        newsletter/2020_02_02.md.
    When: last_newsletters is called
    Then: A LastNewsletter object is returned that returns a datetime object with
        2020-02-03 as last day for the daily periodicity.
    """
    newsletter_dir = create_files(["2020_01_01.md", "2020_01_02.md"], repo)

    result = last_newsletter_changes(newsletter_dir)

    assert result.daily == datetime(2020, 1, 3, tzinfo=tz.tzlocal())


@pytest.mark.freeze_time("2021-02-10T12:00:00")
def test_digital_garden_changes_to_publish_selects_last_week_changes() -> None:
    """
    Given: A mkdocs repo with changes done in the last and current weeks.
    When: changes_to_publish is called.
    Then: Only last week changes are selected to be published for the weekly feed.
    """
    last_week_change = Change(
        date=datetime(2021, 2, 2, tzinfo=tz.tzlocal()),
        summary="Add funny emojis.",
        type_="feature",
        scope=None,
    )
    this_week_change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add ash, birch and beech information.",
        type_="feature",
        scope="botany",
    )
    changes = [last_week_change, this_week_change]

    result = digital_garden_changes(changes)

    assert last_week_change in result.weekly
    assert this_week_change not in result.weekly


@pytest.mark.freeze_time("2021-02-10T12:00:00")
def test_digital_garden_changes_dont_select_last_week_published_changes() -> None:
    """
    Given: A mkdocs repo with changes done in the last and current weeks, and last
        week changes have been already published.
    When: changes_to_publish is called.
    Then: No changes are going to be published
    """
    last_week_change = Change(
        date=datetime(2021, 2, 2, tzinfo=tz.tzlocal()),
        summary="Add funny emojis.",
        type_="feature",
        scope=None,
    )
    this_week_change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add ash, birch and beech information.",
        type_="feature",
        scope="botany",
    )
    changes = [last_week_change, this_week_change]
    last_published = LastNewsletter(weekly=datetime(2021, 2, 8, tzinfo=tz.tzlocal()))

    result = digital_garden_changes(changes, last_published)

    assert result.weekly == []


@pytest.mark.freeze_time("2021-02-10T12:00:00")
def test_digital_garden_changes_to_publish_selects_last_month_changes() -> None:
    """
    Given: A mkdocs git repo with changes done in the last and the current months.
    When: changes_to_publish is called.
    Then: Only last month changes are selected to be published for the yearly feed.
    """
    last_month_change = Change(
        date=datetime(2021, 1, 2, tzinfo=tz.tzlocal()),
        summary="Add funny emojis.",
        type_="feature",
        scope=None,
    )
    this_month_change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add ash, birch and beech information.",
        type_="feature",
        scope="botany",
    )
    changes = [last_month_change, this_month_change]

    result = digital_garden_changes(changes)

    assert last_month_change in result.monthly
    assert this_month_change not in result.monthly


@pytest.mark.freeze_time("2021-02-10T12:00:00")
def test_digital_garden_changes_dont_select_last_month_published_changes() -> None:
    """
    Given: A mkdocs repo with changes done in the last and current months, and last
        month changes have been already published.
    When: changes_to_publish is called.
    Then: No changes are going to be published
    """
    last_month_change = Change(
        date=datetime(2021, 1, 2, tzinfo=tz.tzlocal()),
        summary="Add funny emojis.",
        type_="feature",
        scope=None,
    )
    this_month_change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add ash, birch and beech information.",
        type_="feature",
        scope="botany",
    )
    changes = [last_month_change, this_month_change]
    last_published = LastNewsletter(monthly=datetime(2021, 2, 1, tzinfo=tz.tzlocal()))

    result = digital_garden_changes(changes, last_published)

    assert result.monthly == []


@pytest.mark.freeze_time("2021-02-10T12:00:00")
def test_digital_garden_changes_to_publish_selects_last_year_changes() -> None:
    """
    Given: A mkdocs git repo with changes done in the last and the current years.
    When: changes_to_publish is called.
    Then: Only last year changes are selected to be published for the yearly feed.
    """
    last_year_change = Change(
        date=datetime(2020, 1, 2, tzinfo=tz.tzlocal()),
        summary="Add funny emojis.",
        type_="feature",
        scope=None,
    )
    this_year_change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add ash, birch and beech information.",
        type_="feature",
        scope="botany",
    )
    changes = [last_year_change, this_year_change]

    result = digital_garden_changes(changes)

    assert last_year_change in result.yearly
    assert this_year_change not in result.yearly


@pytest.mark.freeze_time("2021-02-05T12:00:00")
def test_digital_garden_changes_dont_select_last_year_published_changes() -> None:
    """
    Given: A mkdocs repo with changes done in the last and current years, and last
        year changes have been already published.
    When: changes_to_publish is called.
    Then: No changes are going to be published
    """
    last_year_change = Change(
        date=datetime(2020, 1, 2, tzinfo=tz.tzlocal()),
        summary="Add funny emojis.",
        type_="feature",
        scope=None,
    )
    this_year_change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add ash, birch and beech information.",
        type_="feature",
        scope="botany",
    )
    changes = [last_year_change, this_year_change]
    last_published = LastNewsletter(yearly=datetime(2021, 1, 1, tzinfo=tz.tzlocal()))

    result = digital_garden_changes(changes, last_published)

    assert result.yearly == []


@pytest.mark.parametrize("change_type", ["chore", "style"])
def test_digital_garden_ignores_other_change_types(change_type: str) -> None:
    """
    Given: A change with a type_ other than those in CHANGE_TYPE_TEXT.
    When: create_newsletter is called.
    Then: The changes are not part of the output.
    """
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="A change that should not be in the newsletter",
        type_=change_type,
        scope="devops",
    )

    result = digital_garden_changes([change])

    assert len(result.daily) == 0


def test_add_categories_detect_first_level(config: MkDocsConfig) -> None:
    """
    Given: a change whose affected file belongs to a first level document in the nav.
    When: add_change_categories is called.
    Then: The title of the nav is added as the category and the subcategory and
        file_section are None. The file name is added under the file_ attribute.
    """
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add (╯°□°)╯ ┻━┻ emoji",
        type_="feature",
        scope="emojis",
    )

    result = add_change_categories([change], config)

    assert result[0].file_ == "emojis.md"
    assert result[0].category == "Emojis"
    assert result[0].category_order == 4
    assert result[0].file_section is None
    assert result[0].subcategory is None


def test_add_categories_detect_first_level_on_sections(config: MkDocsConfig) -> None:
    """
    Given: a change whose affected file belongs to a first level document that is
        indexed as a section in the nav.
    When: add_change_categories is called.
    Then: The title of the nav is added as the category and the subcategory and
        file_section are None. The file name is added under the file_ attribute.
    """
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="add devops",
        type_="feature",
        scope="devops",
    )

    result = add_change_categories([change], config)

    assert result[0].file_ == "devops.md"
    assert result[0].category == "DevOps"
    assert result[0].category_order == 1
    assert result[0].file_section is None
    assert result[0].subcategory is None


def test_add_categories_detect_second_level(config: MkDocsConfig) -> None:
    """
    Given: a change whose affected file belongs to a second level document in the nav.
    When: add_change_categories is called.
    Then:
        * The title of the nav is added as the subcategory
        * The title of the category is added as category
        * The file_section is None.
        * The file name is added under the file_ attribute.
    """
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add TDD description",
        type_="feature",
        scope="tdd",
    )

    result = add_change_categories([change], config)

    assert result[0].file_ == "tdd.md"
    assert result[0].category == "Coding"
    assert result[0].category_order == 2
    assert result[0].subcategory == "TDD"
    assert result[0].subcategory_order == 0
    assert result[0].file_section is None


def test_add_categories_detect_third_level(config: MkDocsConfig) -> None:
    """
    Given: a change whose affected file belongs to a third level document in the nav.
    When: add_change_categories is called.
    Then:
        * The title of the nav is added as the file_section
        * The title of the category is added as category
        * The title of the subcategory is added as subcategory
        * The file name is added under the file_ attribute.
    """
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add helm",
        type_="feature",
        scope="helm",
    )

    result = add_change_categories([change], config)

    assert result[0].file_ == "helm.md"
    assert result[0].category == "DevOps"
    assert result[0].category_order == 1
    assert result[0].subcategory == "Infrastructure as Code"
    assert result[0].subcategory_order == 1
    assert result[0].file_section == "Helm"
    assert result[0].file_section_order == 0


def test_add_categories_detect_fourth_level(config: MkDocsConfig) -> None:
    """
    Given: a change whose affected file belongs to a fourth level document in the nav.
    When: add_change_categories is called.
    Then:
        * The title of the nav is added as the file_section
        * The title of the category is added as category
        * The title of the subcategory is added as subcategory
        * The file name is added under the file_ attribute.
    """
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add gitpython",
        type_="feature",
        scope="gitpython",
    )

    result = add_change_categories([change], config)

    assert result[0].file_ == "gitpython.md"
    assert result[0].file_section == "GitPython"
    assert result[0].file_section_order == 0
    assert result[0].category == "Coding"
    assert result[0].category_order == 2
    assert result[0].subcategory == "Python"
    assert result[0].subcategory_order == 1


def test_add_categories_detect_fifth_level_or_above(config: MkDocsConfig) -> None:
    """
    Given: a change whose affected file belongs to a fifth level or above document in
        the nav.
    When: add_change_categories is called.
    Then:
        * The title of the nav is added as the file_section
        * The title of the category is added as category
        * The title of the subcategory is added as subcategory
        * The file name is added under the file_ attribute.
    """
    # ECE001: Expression is too complex, we need to do it this way
    config["nav"][2]["Coding"][1]["Python"][0]["Libraries"].append(  # noqa: ECE001
        {"Data Libraries": [{"DeepDiff": "deepdiff.md"}]}
    )
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add deepdiff",
        type_="feature",
        scope="deepdiff",
    )

    result = add_change_categories([change], config)

    assert result[0].file_ == "deepdiff.md"
    assert result[0].file_section == "DeepDiff"
    assert result[0].file_section_order == 0
    assert result[0].category == "Coding"
    assert result[0].category_order == 2
    assert result[0].subcategory == "Python"
    assert result[0].subcategory_order == 1


def test_add_categories_extracts_file_subsection(config: MkDocsConfig) -> None:
    """
    Given: a change whose scope contains the subsection information.
    When: add_change_categories is called.
    Then: The file_subsection is extracted and the file_ is correct.
    """
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add gitpython installation",
        type_="feature",
        scope="gitpython#Installation procedure",
    )

    result = add_change_categories([change], config)

    assert result[0].file_ == "gitpython.md"
    assert result[0].file_subsection == "#installation-procedure"


def test_add_categories_groups_changes_with_scope_not_in_nav(
    config: MkDocsConfig,
) -> None:
    """
    Given: a change whose scope references a file that is not in the nav.
    When: add_change_categories is called.
    Then: The change is grouped under the Others category as the last category.
    """
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Add gitpython installation",
        type_="feature",
        scope="unexistent_scope",
    )

    result = add_change_categories([change], config)

    assert result[0].file_ is None
    assert result[0].category == "Other"
    assert result[0].category_order == 999
    assert result[0].file_section is None
    assert result[0].subcategory is None


def test_create_newsletter_creates_daily_article(repo: Repo) -> None:
    """
    Given: a change to publish in the daily summary.
    When: create_newsletters is called
    Then: The file is created and a File object is returned.
    """
    desired_file = f"{repo.working_dir}/docs/newsletter/2021_02_08.md"
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Create the introduction page",
        type_="feature",
        scope="index",
        category="Introduction",
        category_order=0,
        file_="index.md",
    )
    file_content = dedent(
        """\
        # [Introduction](index.md)

        * New: Create the introduction page"""
    )
    changes_to_publish = DigitalGardenChanges(daily=[change])

    result = create_newsletters(changes_to_publish, repo)

    assert result[0] == desired_file
    with open(
        os.path.join(str(repo.working_dir), "docs/newsletter/2021_02_08.md"),
        encoding="utf-8",
    ) as file_descriptor:
        assert file_descriptor.read() == file_content


def test_create_newsletter_creates_weekly_articles(repo: Repo) -> None:
    """
    Given: a change to publish in the weekly summary.
    When: create_newsletters is called
    Then: The file is created and a File object is returned.
    """
    desired_file = f"{repo.working_dir}/docs/newsletter/2021_w06.md"
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Create the introduction page",
        type_="feature",
        scope="index",
        category="Introduction",
        category_order=0,
        file_="index.md",
    )
    file_content = dedent(
        """\
        # [Introduction](index.md)

        * New: Create the introduction page"""
    )
    changes_to_publish = DigitalGardenChanges(weekly=[change])

    result = create_newsletters(changes_to_publish, repo)

    assert result[0] == desired_file
    with open(
        os.path.join(str(repo.working_dir), "docs/newsletter/2021_w06.md"),
        encoding="utf-8",
    ) as file_descriptor:
        assert file_descriptor.read() == file_content


def test_create_newsletter_creates_monthly_articles(repo: Repo) -> None:
    """
    Given: a change to publish in the monthly summary.
    When: create_newsletters is called
    Then: The file is created and a File object is returned.
    """
    desired_file = f"{repo.working_dir}/docs/newsletter/2021_02.md"
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Create the introduction page",
        type_="feature",
        scope="index",
        category="Introduction",
        category_order=0,
        file_="index.md",
    )
    file_content = dedent(
        """\
        # [Introduction](index.md)

        * New: Create the introduction page"""
    )
    changes_to_publish = DigitalGardenChanges(monthly=[change])

    result = create_newsletters(changes_to_publish, repo)

    assert result[0] == desired_file
    with open(
        os.path.join(str(repo.working_dir), "docs/newsletter/2021_02.md"),
        encoding="utf-8",
    ) as file_descriptor:
        assert file_descriptor.read() == file_content


def test_create_newsletter_creates_yearly_articles(repo: Repo) -> None:
    """
    Given: a change to publish in the yearly summary.
    When: create_newsletters is called
    Then: The file is created and a File object is returned.
    """
    desired_file = f"{repo.working_dir}/docs/newsletter/2021.md"
    change = Change(
        date=datetime(2021, 2, 8, tzinfo=tz.tzlocal()),
        summary="Create the introduction page",
        type_="feature",
        scope="index",
        category="Introduction",
        category_order=0,
        file_="index.md",
    )
    file_content = dedent(
        """\
        # [Introduction](index.md)

        * New: Create the introduction page"""
    )
    changes_to_publish = DigitalGardenChanges(yearly=[change])

    result = create_newsletters(changes_to_publish, repo)

    assert result[0] == desired_file
    with open(
        os.path.join(str(repo.working_dir), "docs/newsletter/2021.md"), encoding="utf-8"
    ) as file_descriptor:
        assert file_descriptor.read() == file_content
