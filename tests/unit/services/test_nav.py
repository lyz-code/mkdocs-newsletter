"""Test the building of the newsletter nav.

The sections and pages need to be defined in the `items` attribute and an ordered
list of Pages and SectionPages need to be stored in the `pages` attribute.
"""

import pytest
from git import Repo
from mkdocs.config.base import Config
from mkdocs.structure.files import File
from mkdocs.structure.nav import Navigation

from mkdocs_newsletter.services.nav import build_nav


@pytest.fixture(name="nav")
def nav_() -> Navigation:
    """Create an empty Navigation object."""
    return Navigation([], [])


def test_build_nav_skips_files_whose_filename_doesnt_match_regexp(
    repo: Repo, config: Config, nav: Navigation
) -> None:
    """
    Given: A file that doesn't match the newsletter file format.
    When: build_nav is called
    Then: The nav doesn't show the file
    """
    desired_file = File(
        path="invalid_file.md",
        src_dir=f"{repo.working_dir}/docs/newsletter",
        dest_dir=f"{repo.working_dir}/site/newsletter",
        use_directory_urls=False,
    )

    result = build_nav(nav, config, [desired_file])

    assert result.items[0].title == "Newsletters"
    assert result.items[0].children == []


def test_build_nav_accepts_newsletter_landing_page(
    repo: Repo, config: Config, nav: Navigation
) -> None:
    """
    Given: A newsletter landing page file.
    When: build_nav is called
    Then: The nav Newsletter section uses the page.
    """
    desired_file = File(
        path="0_index.md",
        src_dir=f"{repo.working_dir}/docs/newsletter",
        dest_dir=f"{repo.working_dir}/site/newsletter",
        use_directory_urls=False,
    )

    result = build_nav(nav, config, [desired_file])

    assert result.items[0].title == "Newsletters"
    assert result.items[0].file == desired_file
    assert result.pages[-1].file == desired_file


def test_build_nav_creates_year_entry(
    repo: Repo, config: Config, nav: Navigation
) -> None:
    """
    Given: A new year file.
    When: build_nav is called
    Then: the year nav SectionPage entry is created
    """
    desired_file = File(
        path="2021.md",
        src_dir=f"{repo.working_dir}/docs/newsletter",
        dest_dir=f"{repo.working_dir}/site/newsletter",
        use_directory_urls=False,
    )

    result = build_nav(nav, config, [desired_file])

    assert result.items[0].title == "Newsletters"
    assert result.items[0].children[0].file == desired_file
    assert result.items[0].children[0].title == "2021"
    assert result.pages[-1].file == desired_file


def test_build_nav_sorts_year_entries(
    repo: Repo, config: Config, nav: Navigation
) -> None:
    """
    Given: two year files.
    When: build_nav is called
    Then: the year nav entries are sorted descending.
    """
    desired_files = [
        File(
            path="2020.md",
            src_dir=f"{repo.working_dir}/docs/newsletter",
            dest_dir=f"{repo.working_dir}/site/newsletter",
            use_directory_urls=False,
        ),
        File(
            path="2021.md",
            src_dir=f"{repo.working_dir}/docs/newsletter",
            dest_dir=f"{repo.working_dir}/site/newsletter",
            use_directory_urls=False,
        ),
    ]

    result = build_nav(nav, config, desired_files)

    assert result.items[0].children[0].file == desired_files[1]
    assert result.items[0].children[0].title == "2021"
    assert result.pages[-2].file == desired_files[1]
    assert result.items[0].children[1].file == desired_files[0]
    assert result.items[0].children[1].title == "2020"
    assert result.pages[-1].file == desired_files[0]


def test_build_nav_creates_month_entry(
    repo: Repo, config: Config, nav: Navigation
) -> None:
    """
    Given: A new month file.
    When: build_nav is called
    Then: the month nav entry is created
    """
    desired_file = File(
        path="2021_01.md",
        src_dir=f"{repo.working_dir}/docs/newsletter",
        dest_dir=f"{repo.working_dir}/site/newsletter",
        use_directory_urls=False,
    )

    result = build_nav(nav, config, [desired_file])

    year_nav = result.items[0].children[0]
    assert result.items[0].title == "Newsletters"
    assert year_nav.title == "2021"
    assert year_nav.children[0].title == "January of 2021"
    assert year_nav.children[0].file == desired_file


def test_build_nav_sorts_month_entries(
    repo: Repo, config: Config, nav: Navigation
) -> None:
    """
    Given: Two month files.
    When: build_nav is called
    Then: the month nav entries are sorted.
    """
    desired_files = [
        File(
            path="2021_01.md",
            src_dir=f"{repo.working_dir}/docs/newsletter",
            dest_dir=f"{repo.working_dir}/site/newsletter",
            use_directory_urls=False,
        ),
        File(
            path="2021_02.md",
            src_dir=f"{repo.working_dir}/docs/newsletter",
            dest_dir=f"{repo.working_dir}/site/newsletter",
            use_directory_urls=False,
        ),
    ]

    result = build_nav(nav, config, desired_files)

    year_nav = result.items[0].children[0]
    assert year_nav.title == "2021"
    assert year_nav.children[0].title == "February of 2021"
    assert year_nav.children[0].file == desired_files[1]
    assert year_nav.children[1].title == "January of 2021"
    assert year_nav.children[1].file == desired_files[0]


def test_build_nav_creates_week_entry(
    repo: Repo, config: Config, nav: Navigation
) -> None:
    """
    Given: A new week file.
    When: build_nav is called
    Then: the week nav entry is created
    """
    desired_file = File(
        path="2021_w01.md",
        src_dir=f"{repo.working_dir}/docs/newsletter",
        dest_dir=f"{repo.working_dir}/site/newsletter",
        use_directory_urls=False,
    )

    result = build_nav(nav, config, [desired_file])

    assert result.items[0].title == "Newsletters"
    year_nav = result.items[0].children[0]
    assert year_nav.title == "2021"
    month_nav = year_nav.children[0]
    assert month_nav.title == "January of 2021"
    assert month_nav.children[0].title == "1st Week of 2021"
    assert month_nav.children[0].file == desired_file


def test_build_nav_sorts_week_entries(
    repo: Repo, config: Config, nav: Navigation
) -> None:
    """
    Given: Two week files.
    When: build_nav is called
    Then: the week nav entries are sorted.
    """
    desired_files = [
        File(
            path="2021_w01.md",
            src_dir=f"{repo.working_dir}/docs/newsletter",
            dest_dir=f"{repo.working_dir}/site/newsletter",
            use_directory_urls=False,
        ),
        File(
            path="2021_w02.md",
            src_dir=f"{repo.working_dir}/docs/newsletter",
            dest_dir=f"{repo.working_dir}/site/newsletter",
            use_directory_urls=False,
        ),
    ]

    result = build_nav(nav, config, desired_files)

    year_nav = result.items[0].children[0]
    month_nav = year_nav.children[0]
    assert month_nav.title == "January of 2021"
    assert month_nav.children[0].title == "2nd Week of 2021"
    assert month_nav.children[0].file == desired_files[1]
    assert month_nav.children[1].title == "1st Week of 2021"
    assert month_nav.children[1].file == desired_files[0]


def test_build_nav_creates_day_entry(
    repo: Repo, config: Config, nav: Navigation
) -> None:
    """
    Given: A new day file.
    When: build_nav is called
    Then: the day nav entry is created
    """
    desired_file = File(
        path="2021_01_05.md",
        src_dir=f"{repo.working_dir}/docs/newsletter",
        dest_dir=f"{repo.working_dir}/site/newsletter",
        use_directory_urls=False,
    )

    result = build_nav(nav, config, [desired_file])

    assert result.items[0].title == "Newsletters"
    year_nav = result.items[0].children[0]
    assert year_nav.title == "2021"
    month_nav = year_nav.children[0]
    assert month_nav.title == "January of 2021"
    week_nav = month_nav.children[0]
    assert week_nav.title == "1st Week of 2021"
    assert week_nav.children[0].title == "5th January 2021"
    assert week_nav.children[0].file == desired_file


def test_build_nav_sorts_day_entries(
    repo: Repo, config: Config, nav: Navigation
) -> None:
    """
    Given: Two day files.
    When: build_nav is called
    Then: the day nav entries are sorted.
    """
    desired_files = [
        File(
            path="2021_01_05.md",
            src_dir=f"{repo.working_dir}/docs/newsletter",
            dest_dir=f"{repo.working_dir}/site/newsletter",
            use_directory_urls=False,
        ),
        File(
            path="2021_01_06.md",
            src_dir=f"{repo.working_dir}/docs/newsletter",
            dest_dir=f"{repo.working_dir}/site/newsletter",
            use_directory_urls=False,
        ),
    ]

    result = build_nav(nav, config, desired_files)

    year_nav = result.items[0].children[0]
    month_nav = year_nav.children[0]
    week_nav = month_nav.children[0]
    assert week_nav.title == "1st Week of 2021"
    assert week_nav.children[0].title == "6th January 2021"
    assert week_nav.children[0].file == desired_files[1]
    assert week_nav.children[1].title == "5th January 2021"
    assert week_nav.children[1].file == desired_files[0]


def test_build_nav_populates_next_and_previous_pages(
    repo: Repo, config: Config, nav: Navigation
) -> None:
    """
    Given: Two day files.
    When: build_nav is called
    Then: the day nav entries have the correct previous and next attributes set.
    """
    desired_files = [
        File(
            path="2021_01_05.md",
            src_dir=f"{repo.working_dir}/docs/newsletter",
            dest_dir=f"{repo.working_dir}/site/newsletter",
            use_directory_urls=False,
        ),
        File(
            path="2021_01_06.md",
            src_dir=f"{repo.working_dir}/docs/newsletter",
            dest_dir=f"{repo.working_dir}/site/newsletter",
            use_directory_urls=False,
        ),
    ]

    result = build_nav(nav, config, desired_files)

    assert result.pages[0].next_page == result.pages[1]
    assert result.pages[1].previous_page == result.pages[0]
