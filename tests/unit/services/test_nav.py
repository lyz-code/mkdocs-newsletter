"""Test the building of the newsletter nav.

The sections and pages need to be defined in the `items` attribute and an ordered
list of Pages and SectionPages need to be stored in the `pages` attribute.
"""

from git import Repo
from mkdocs.config.defaults import MkDocsConfig

from mkdocs_newsletter.services.nav import build_nav

from .test_last_newsletters import create_files


def test_build_nav_skips_files_whose_filename_doesnt_match_regexp(
    repo: Repo,
    config: MkDocsConfig,
) -> None:
    """
    Given: A file that doesn't match the newsletter file format.
    When: build_nav is called
    Then: The nav doesn't show the file
    """
    newsletter_dir = create_files(["invalid_file.md"], repo)

    result = build_nav(config, newsletter_dir)

    assert result["nav"][-1] == {"Newsletters": []}


def test_build_nav_accepts_newsletter_landing_page(
    repo: Repo,
    config: MkDocsConfig,
) -> None:
    """
    Given: A newsletter landing page file.
    When: build_nav is called
    Then: The nav Newsletter section uses the page.
    """
    newsletter_dir = create_files(["0_newsletter_index.md"], repo)

    result = build_nav(config, newsletter_dir)

    assert result["nav"][-1] == {"Newsletters": ["newsletter/0_newsletter_index.md"]}


def test_build_nav_creates_year_entry(
    repo: Repo,
    config: MkDocsConfig,
) -> None:
    """
    Given: A new year file.
    When: build_nav is called
    Then: the year nav SectionPage entry is created
    """
    newsletter_dir = create_files(["2021.md"], repo)

    result = build_nav(config, newsletter_dir)

    assert result["nav"][-1] == {"Newsletters": [{"2021": ["newsletter/2021.md"]}]}


def test_build_nav_sorts_year_entries(
    repo: Repo,
    config: MkDocsConfig,
) -> None:
    """
    Given: two year files.
    When: build_nav is called
    Then: the year nav entries are sorted descending.
    """
    newsletter_dir = create_files(["2020.md", "2021.md"], repo)

    result = build_nav(config, newsletter_dir)

    assert result["nav"][-1] == {
        "Newsletters": [
            {"2021": ["newsletter/2021.md"]},
            {"2020": ["newsletter/2020.md"]},
        ]
    }


def test_build_nav_creates_month_entry(
    repo: Repo,
    config: MkDocsConfig,
) -> None:
    """
    Given: A new month file.
    When: build_nav is called
    Then: the month nav entry is created
    """
    newsletter_dir = create_files(["2021_01.md"], repo)

    result = build_nav(config, newsletter_dir)

    assert result["nav"][-1]["Newsletters"] == [
        {"2021": [{"January of 2021": ["newsletter/2021_01.md"]}]},
    ]


def test_build_nav_sorts_month_entries(
    repo: Repo,
    config: MkDocsConfig,
) -> None:
    """
    Given: Two month files.
    When: build_nav is called
    Then: the month nav entries are sorted.
    """
    newsletter_dir = create_files(["2021_01.md", "2021_02.md"], repo)

    result = build_nav(config, newsletter_dir)

    assert result["nav"][-1]["Newsletters"] == [
        {
            "2021": [
                {"February of 2021": ["newsletter/2021_02.md"]},
                {"January of 2021": ["newsletter/2021_01.md"]},
            ]
        },
    ]


def test_build_nav_creates_week_entry(
    repo: Repo,
    config: MkDocsConfig,
) -> None:
    """
    Given: A new week file.
    When: build_nav is called
    Then: the week nav entry is created
    """
    newsletter_dir = create_files(["2021_w01.md"], repo)

    result = build_nav(config, newsletter_dir)

    assert result["nav"][-1]["Newsletters"][0]["2021"] == [
        {"January of 2021": [{"1st Week of 2021": ["newsletter/2021_w01.md"]}]},
    ]


def test_build_nav_sorts_week_entries(
    repo: Repo,
    config: MkDocsConfig,
) -> None:
    """
    Given: Two week files.
    When: build_nav is called
    Then: the week nav entries are sorted.
    """
    newsletter_dir = create_files(["2021_w01.md", "2021_w02.md"], repo)

    result = build_nav(config, newsletter_dir)

    assert result["nav"][-1]["Newsletters"][0]["2021"] == [
        {
            "January of 2021": [
                {"2nd Week of 2021": ["newsletter/2021_w02.md"]},
                {"1st Week of 2021": ["newsletter/2021_w01.md"]},
            ]
        },
    ]


def test_build_nav_creates_day_entry(
    repo: Repo,
    config: MkDocsConfig,
) -> None:
    """
    Given: A new day file.
    When: build_nav is called
    Then: the day nav entry is created
    """
    newsletter_dir = create_files(["2021_01_05.md"], repo)

    result = build_nav(config, newsletter_dir)

    year_nav = result["nav"][-1]["Newsletters"][0]["2021"]
    assert year_nav[0]["January of 2021"] == [
        {"1st Week of 2021": [{"5th January 2021": "newsletter/2021_01_05.md"}]},
    ]


def test_build_nav_sorts_day_entries(
    repo: Repo,
    config: MkDocsConfig,
) -> None:
    """
    Given: Two day files.
    When: build_nav is called
    Then: the day nav entries are sorted.
    """
    newsletter_dir = create_files(["2021_01_11.md", "2021_01_12.md"], repo)

    result = build_nav(config, newsletter_dir)

    year_nav = result["nav"][-1]["Newsletters"][0]["2021"]
    assert year_nav[0]["January of 2021"] == [
        {
            "2nd Week of 2021": [
                {"12th January 2021": "newsletter/2021_01_12.md"},
                {"11th January 2021": "newsletter/2021_01_11.md"},
            ]
        },
    ]
