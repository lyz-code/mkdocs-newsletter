"""Gather services to create the newsletters MkDocs nav section."""

import calendar
import datetime
import os
import re
from typing import Any, Dict, List, Tuple, Union

from mkdocs.config.defaults import MkDocsConfig

NavData = Dict[Union[int, str], Any]
Sections = List[Union[str, Dict[str, Any]]]


def build_nav(config: MkDocsConfig, newsletter_dir: str) -> MkDocsConfig:
    """Build the navigation section of the newsletters.

    Args:
        config: MkDocs configuration object.
        newsletter_dir: Directory containing the newsletter articles.

    Returns:
        The config object with the newsletters.
    """
    nav_data: Dict[Union[int, str], Any] = {}

    newsletter_regex = (
        r"(?P<year>\d{4})"
        r"(_w(?P<week_number>\d{2}))?"
        r"(_(?P<month>\d{2}))?"
        r"(_(?P<day>\d{2}))?.md"
    )
    for file_ in os.scandir(newsletter_dir):
        file_path = f"newsletter/{file_.name}"
        match = re.match(newsletter_regex, file_.name)
        if match is None:
            if file_.name == "0_newsletter_index.md":
                nav_data["index"] = file_path
            continue

        year_match = match.group("year")
        week_match = match.group("week_number")
        month_match = match.group("month")
        day_match = match.group("day")

        if year_match is not None:
            year = int(year_match)
            nav_data.setdefault(year, {})
            if month_match is not None:
                month = int(month_match)
                nav_data[year].setdefault(month, {})
                if day_match is not None:
                    day = int(day_match)
                    week = datetime.datetime(year, month, day).isocalendar()[1]
                    nav_data[year][month].setdefault(week, {})
                    nav_data[year][month][week][day] = file_path
                else:
                    nav_data[year][month]["index"] = file_path
            elif week_match is not None:
                week = int(week_match)
                month = datetime.datetime.strptime(f"{year}{week}-1", "%Y%W-%w").month
                nav_data[year].setdefault(month, {})
                nav_data[year][month].setdefault(week, {})
                nav_data[year][month][week]["index"] = file_path
            else:
                nav_data[year]["index"] = file_path

    return _nav_data_to_nav(nav_data, config)


def _nav_data_to_nav(nav_data: NavData, config: MkDocsConfig) -> MkDocsConfig:
    """Convert the nav_data dictionary to the Mkdocs nav section.

    Args:
        nav_data: dictionary with the newsletter file data with the following structure.
            {
                'index': 0_newsletter_index.md
                year: {
                    'index': year.md
                    month_number: {
                        'index': year_month.md
                        week_number: {
                            'index': year_wweek_number.md
                            day: year_month_day.md
                        }
                    }
                }
            }
        config: MkDocs configuration object.

    Returns:
        MkDocs config object with the list of newsletters under the Newsletters section.
    """
    newsletter_nav, nav_data = _initialize_section(nav_data)

    for year, year_data in sorted(nav_data.items(), reverse=True):
        year_nav, year_data = _initialize_section(year_data)

        for month, month_data in sorted(year_data.items(), reverse=True):
            month_nav, month_data = _initialize_section(month_data)

            for week, week_data in sorted(month_data.items(), reverse=True):
                week_nav, week_data = _initialize_section(week_data)

                for day, day_data in sorted(week_data.items(), reverse=True):
                    day_title = (
                        f"{_int_to_ordinal(day)} {calendar.month_name[month]} {year}"
                    )
                    week_nav.append({day_title: day_data})
                month_nav.append({f"{_int_to_ordinal(week)} Week of {year}": week_nav})
            year_nav.append({f"{calendar.month_name[month]} of {year}": month_nav})
        newsletter_nav.append({str(year): year_nav})
    config["nav"].append({"Newsletters": newsletter_nav})

    return config


def _initialize_section(section_data: NavData) -> Tuple[Sections, NavData]:
    """Create the section object with the section data.

    If the section_data contains an 'index' key it will index the section page,
    otherwise it will create an empty list.

    Args:
        section_data: Dictionary with the section data
        config: MkDocs config object.

    Returns:
        List of sections.
        Updated section_data without the 'index' key.
    """
    try:
        section_nav = [section_data["index"]]
        section_data.pop("index")
    except KeyError:
        section_nav = []

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
