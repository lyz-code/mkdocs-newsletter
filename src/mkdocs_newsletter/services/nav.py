"""Gather services to create the newsletters MkDocs nav section."""

import calendar
import datetime
import re
from contextlib import suppress
from typing import Any, Dict, List, Tuple, Union

from mkdocs.config.base import Config
from mkdocs.structure.files import File
from mkdocs.structure.nav import Navigation, Section
from mkdocs.structure.pages import Page
from mkdocs_section_index import SectionPage

NavData = Dict[Union[int, str], Any]
Sections = Union[SectionPage, Section]


def build_nav(nav: Navigation, config: Config, files: List[File]) -> Navigation:
    """Build the navigation section of the newsletters.

    Args:
        nav: MkDocs navigation object
        config: MkDocs configuration object.
        files: all mkdocs files.

    Returns:
        The nav object with the newsletters.
    """
    nav_data: Dict[Union[int, str], Any] = {}

    newsletter_regex = (
        r"(?P<year>\d{4})"
        r"(_w(?P<week_number>\d{2}))?"
        r"(_(?P<month>\d{2}))?"
        r"(_(?P<day>\d{2}))?"
    )
    for file_ in files:
        match = re.match(newsletter_regex, file_.name)
        if match is None:
            if file_.name == "0_index":
                nav_data["index"] = file_
            continue

        year = match.group("year")
        week = match.group("week_number")
        month = match.group("month")
        day = match.group("day")

        if year is not None:
            year = int(year)
            nav_data.setdefault(year, {})
            if month is not None:
                month = int(month)
                nav_data[year].setdefault(month, {})
                if day is not None:
                    day = int(day)
                    week = datetime.datetime(year, month, day).isocalendar()[1]
                    nav_data[year][month].setdefault(week, {})
                    nav_data[year][month][week][day] = file_
                else:
                    nav_data[year][month]["index"] = file_
            elif week is not None:
                week = int(week)
                month = datetime.datetime.strptime(f"{year}{week}-1", "%Y%W-%w").month
                nav_data[year].setdefault(month, {})
                nav_data[year][month].setdefault(week, {})
                nav_data[year][month][week]["index"] = file_
            else:
                nav_data[year]["index"] = file_

    return _nav_data_to_nav(nav_data, config, nav)


def _nav_data_to_nav(nav_data: NavData, config: Config, nav: Navigation) -> List[Any]:
    """Convert the nav_data dictionary to the Mkdocs nav section.

    Args:
        nav_data: dictionary with the newsletter file data with the following structure.
            {
                'index': File(0_index.md)
                year: {
                    'index': File(year.md),
                    month_number: {
                        'index': File(year_month.md),
                        week_number: {
                            'index': File(year_wweek_number.md),
                            day: File(year_month_day.md),
                        }
                    }
                }
            }
        config: MkDocs configuration object.
        nav: MkDocs navigation object

    Returns:
        MkDocs nav object with the list of newsletters.
    """
    newsletter_nav, nav_data = _initialize_section("Newsletters", nav_data, config)

    for year, year_data in sorted(nav_data.items(), reverse=True):
        year_nav, year_data = _initialize_section(str(year), year_data, config)

        for month, month_data in sorted(year_data.items(), reverse=True):
            month_nav, month_data = _initialize_section(
                f"{calendar.month_name[month]} of {year}", month_data, config
            )

            for week, week_data in sorted(month_data.items(), reverse=True):
                week_nav, week_data = _initialize_section(
                    f"{_int_to_ordinal(week)} Week of {year}", week_data, config
                )

                for day, day_data in sorted(week_data.items(), reverse=True):
                    week_nav.children.append(
                        Page(
                            f"{_int_to_ordinal(day)} {calendar.month_name[month]}"
                            f" {year}",
                            day_data,
                            config,
                        )
                    )
                month_nav.children.append(week_nav)
            year_nav.children.append(month_nav)
        newsletter_nav.children.append(year_nav)
    nav.items.append(newsletter_nav)

    return _build_nav_pages(nav)


def _initialize_section(
    title: str, section_data: NavData, config: Config
) -> Tuple[Sections, NavData]:
    """Create the section object with the section data.

    If the section_data contains an 'index' key it will create a SectionPage, otherwise
    it will create a Section object.

    Args:
        title: Section title
        section_data: Dictionary with the section data
        config: MkDocs config object.

    Returns:
        SectionPage or Section object.
        Updated section_data without the 'index' key.
    """
    try:
        section_nav = SectionPage(title, section_data["index"], config, [])
        section_data.pop("index")
    except KeyError:
        section_nav = Section(title, [])

    return section_nav, section_data


def _int_to_ordinal(number: int) -> str:
    """Convert an integer into its ordinal representation.

    Args:
        number: Number to convert

    Returns:
        ordinal representation of the number
    """
    suffix = ["th", "st", "nd", "rd", "th"][min(number % 10, 4)]
    if 11 <= (number % 100) <= 13:
        suffix = "th"
    return f"{number}{suffix}"


def _build_nav_pages(nav: Navigation) -> Navigation:
    """Build the newsletter `pages` section of the nav.

    Extract the pages from the items of the nav and populate the next and previous pages
    attributes.

    Args:
        nav: MkDocs navigation object

    Returns:
        MkDocs nav object with the newsletter entries in the pages attribute.
    """
    newsletter_section = nav.items[-1]
    nav.pages += _build_section_pages(newsletter_section)

    for index in range(len(nav.pages)):
        with suppress(IndexError):
            nav.pages[index].previous_page = nav.pages[index - 1]
        with suppress(IndexError):
            nav.pages[index].next_page = nav.pages[index + 1]
    return nav


def _build_section_pages(section: Sections) -> List[Union[SectionPage, Page]]:
    """Get the list of pages from a section.

    Args:
        section: MkDocs section object.

    Returns:
        List of pages in the section.
    """
    pages = []

    if isinstance(section, Page):
        pages.append(section)

    if isinstance(section, Section):
        for subsection in section.children:
            pages += _build_section_pages(subsection)

    return pages
