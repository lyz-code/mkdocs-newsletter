"""Gather services related to the management of the newsletters."""

import datetime
import itertools
import operator
import os
import re
from contextlib import suppress
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from dateutil import tz
from dateutil.relativedelta import relativedelta
from deepdiff import grep
from git import Repo
from jinja2 import Environment, PackageLoader, select_autoescape
from mkdocs.config.defaults import MkDocsConfig

from ..model import (
    Change,
    DigitalGardenChanges,
    LastNewsletter,
    Newsletter,
    Newsletters,
    NewsletterSection,
)

CHANGE_TYPE_TEXT = {
    "feature": "New",
    "performance": "Improvement",
    "fix": "Correction",
    "refactor": "Reorganization",
}


def last_newsletter_changes(newsletter_dir: str) -> LastNewsletter:
    """Extract the date of the last change of the last newsletter for each feed.

    Args:
        newsletter_dir: Directory containing the newsletter articles.

    Returns:
        last_newsletter: LastNewsletter object.
    """
    newsletters = _list_newsletters(newsletter_dir)
    last = LastNewsletter()

    # Year feed: Saves the first day of the next year.
    with suppress(IndexError):
        last.yearly = newsletters.yearly[0].date + relativedelta(years=1)

    # Month feed: Saves the first day of the next month.
    with suppress(IndexError):
        last_file_date = newsletters.monthly[0].date
        last.monthly = datetime.datetime(
            last_file_date.year + int(last_file_date.month / 12),
            ((last_file_date.month % 12) + 1),
            1,
            tzinfo=tz.tzlocal(),
        )

    # Week feed: Saves the next Monday from the week of the week number.
    with suppress(IndexError):
        last.weekly = newsletters.weekly[0].date + datetime.timedelta(days=7)

    # Daily feed: Saves the next day.
    with suppress(IndexError):
        last.daily = newsletters.daily[0].date + datetime.timedelta(days=1)

    return last


def _list_newsletters(newsletter_dir: str) -> Newsletters:
    """Create a list of existing newsletters.

    Args:
        newsletter_dir: Directory containing the newsletter articles.

    Returns:
        Newsletters object.
    """
    newsletters = Newsletters()
    with os.scandir(newsletter_dir) as files:
        for file_ in files:
            if file_.name == "0_newsletter_index.md":
                continue
            newsletter = Newsletter(file_=Path(file_.path))
            if newsletter.type_ == "yearly":
                newsletters.yearly.append(newsletter)
            elif newsletter.type_ == "monthly":
                newsletters.monthly.append(newsletter)
            elif newsletter.type_ == "weekly":
                newsletters.weekly.append(newsletter)
            elif newsletter.type_ == "daily":
                newsletters.daily.append(newsletter)
    newsletters.sort()

    return newsletters


def add_change_categories(changes: List[Change], config: MkDocsConfig) -> List[Change]:
    """Add category and subcategory to each change based on their file nav position.

    Args:
        changes: The list of Change objects to process.
        config: MkDocs Config object.

    Returns:
        Updated list of changes.
    """
    for change in changes:
        if change.scope is not None:
            scope_parts = change.scope.split("#")
            change.file_ = f"{scope_parts[0]}.md"
            if len(scope_parts) > 1:
                change.file_subsection = "#" + scope_parts[1].lower().replace(" ", "-")
        nav_search = config["nav"] | grep(change.file_)
        try:
            nav_path = nav_search["matched_values"][0]
        except KeyError:
            change.category = "Other"
            change.category_order = 999
            change.file_ = None
            change.file_subsection = None
            continue

        more_than_three_levels_regex = (
            r"root"
            r"\[(?P<category_order>\d+)\]"
            r"\['(?P<category>[\w\s]+)'\]"
            r"\[(?P<subcategory_order>\d+)\]"
            r"\['(?P<subcategory>[\w\s]+)'\]"
            r"(\[(?P<other_level_order>\d+)\]"
            r"\['(?P<other_level_category>[\w\s]+)'\])+"
            r"\[(?P<file_section_order>\d+)\]"
            r"\['(?P<file_section>[\w\s]+)'\]"
            r"(\[(?P<is_section>\d+)\])?"
        )
        less_than_four_levels_regex = (
            r"root"
            r"\[(?P<category_order>\d+)\]"
            r"\['(?P<category>[\w\s]+)'\]"
            r"(\[(?P<subcategory_order>\d+)\])?"
            r"(\['(?P<subcategory>[\w\s]+)'\])?"
            r"(\[(?P<file_section_order>\d+)\])?"
            r"(\['(?P<file_section>[\w\s]+)'\])?"
            r"(\[(?P<is_section>\d+)\])?"
        )

        match = re.match(more_than_three_levels_regex, nav_path)
        if match is None:
            match = re.match(less_than_four_levels_regex, nav_path)

        if match is not None:
            change.category = match.group("category")
            change.category_order = int(match.group("category_order"))
            change.subcategory = match.group("subcategory")
            if change.subcategory is not None:
                change.subcategory_order = int(match.group("subcategory_order"))
            change.file_section = match.group("file_section")
            if change.file_section is not None:
                change.file_section_order = int(match.group("file_section_order"))
    return changes


def digital_garden_changes(
    changes: List[Change], last_published: Optional[LastNewsletter] = None
) -> DigitalGardenChanges:
    """Extract the changes that need to be published for digital_garden repositories.

    For a change to be published it needs to:

    year: Be made before the first day of the year and after the last published change
        in the year feed.
    month: Be made before the first day of the month and after the last published change
        in the month feed.
    week: Be made before the last Monday and after the last published change in the
        week feed.
    day: Be made before today and after the last published change in the day feed.

    Args:
        changes: The list of Change objects to publish.
        last_published: last published date per feed type

    Returns:
        changes: Ordered changes to publish per feed.
    """
    now = datetime.datetime.now(tz.tzlocal())
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    last_first_weekday = today - datetime.timedelta(days=now.weekday())
    last_first_monthday = today.replace(day=1)
    last_first_yearday = today.replace(day=1, month=1)

    if last_published is None:
        last_published = LastNewsletter()

    return DigitalGardenChanges(
        daily=[
            change
            for change in changes
            if change.date < today
            and (last_published.daily is None or change.date > last_published.daily)
            and change.type_ in CHANGE_TYPE_TEXT
        ],
        weekly=[
            change
            for change in changes
            if change.date < last_first_weekday
            and (last_published.weekly is None or change.date > last_published.weekly)
            and change.type_ in CHANGE_TYPE_TEXT
        ],
        monthly=[
            change
            for change in changes
            if change.date < last_first_monthday
            and (last_published.monthly is None or change.date > last_published.monthly)
            and change.type_ in CHANGE_TYPE_TEXT
        ],
        yearly=[
            change
            for change in changes
            if change.date < last_first_yearday
            and (last_published.yearly is None or change.date > last_published.yearly)
            and change.type_ in CHANGE_TYPE_TEXT
        ],
    )


def create_newsletter_landing_page(config: MkDocsConfig, repo: Repo) -> None:
    """Create the newsletter landing page."""
    base_dir = str(repo.working_dir)
    landing_path = os.path.join(base_dir, "docs/newsletter/0_newsletter_index.md")
    site_url = re.sub("/$", "", config["site_url"])

    if not os.path.isfile(landing_path):
        env = Environment(
            loader=PackageLoader("mkdocs_newsletter", "templates"),
            autoescape=select_autoescape(["html", "xml"]),
        )
        template = env.get_template("newsletter_landing_page.j2")
        landing_page = template.render(site_url=site_url)

        with open(landing_path, "+w", encoding="utf-8") as landing_file:
            landing_file.write(landing_page)


def create_newsletters(changes: DigitalGardenChanges, repo: Repo) -> List[str]:
    """Create the newsletter articles from the semantic changes for all feeds.

    Fills the newsletter article jinja2 template and creates the related File objects.

    Args:
        changes: The list of Change objects to publish per feed.
        repo: Git Repo object with the MkDocs repository.

    Returns:
        List of file paths with the newsletter articles.
    """
    base_dir = str(repo.working_dir)

    files = (
        _create_feed_articles(changes.daily, _get_daily_newsletter_file, base_dir)
        + _create_feed_articles(changes.weekly, _get_weekly_newsletter_file, base_dir)
        + _create_feed_articles(changes.monthly, _get_monthly_newsletter_file, base_dir)
        + _create_feed_articles(changes.yearly, _get_yearly_newsletter_file, base_dir)
    )

    return files


def _create_feed_articles(
    changes: List[Change], group_function: Callable[..., str], base_dir: str
) -> List[str]:
    """Create the newsletter articles from the semantic changes for a feed.

    Fills the newsletter article jinja2 template and creates the related File objects.

    Args:
        changes: The list of Change objects to publish in the feed.
        group_function: Function to group the changes in files.
        base_dir: Directory of the MkDocs repository.

    Returns:
        List of file paths with the newsletter articles.
    """
    files = []
    changes_groups = {}

    newsletter_dir = os.path.join(base_dir, "docs/newsletter")
    if not os.path.exists(newsletter_dir):
        os.makedirs(newsletter_dir)

    for file_name, feed_changes in itertools.groupby(changes, key=group_function):
        changes_groups[file_name] = list(feed_changes)

    for file_name, changes_group in changes_groups.items():
        newsletter_path = os.path.join(newsletter_dir, file_name)
        with open(newsletter_path, "w+", encoding="utf-8") as newsletter_file:
            newsletter_file.write(create_newsletter(changes_group))
        files.append(newsletter_path)

    return files


def create_newsletter(changes: List[Change]) -> str:
    """Build the newsletter article test from the changes.

    Group first by category, then by subcategory and then by file.

    Args:
        changes: List of changes to publish in the article

    Returns:
        Article markdown text.
    """
    env = Environment(
        loader=PackageLoader("mkdocs_newsletter", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("newsletter_article.j2")

    sections = _build_newsletter_sections(changes)

    article = template.render(sections=sections, change_type_text=CHANGE_TYPE_TEXT)
    article = re.sub(r"\n\n+", r"\n\n", article).strip()

    return article


def _build_newsletter_sections(
    changes: List[Change],
) -> List[NewsletterSection]:
    """Create the newsletter sections from the changes.

    Args:
        changes: The list of Change objects to publish in the article.

    Returns:
        A list of sections containing the changes.
    """
    sections = []

    # Sort by category, subcategory, file and date

    category_changes_groups = _group_semantic_changes(changes, "category")

    for category_changes in category_changes_groups:
        category_section, subcategory_changes = _build_newsletter_section(
            category_changes, "category", "subcategory"
        )

        subcategory_changes_groups = _group_semantic_changes(
            subcategory_changes, "subcategory"
        )
        for subcategory_changes in subcategory_changes_groups:
            subcategory_section, file_changes = _build_newsletter_section(
                subcategory_changes, "subcategory", "file_section"
            )

            file_changes_groups = _group_semantic_changes(file_changes, "file_section")
            for file_changes in file_changes_groups:
                file_section, dummy = _build_newsletter_section(
                    file_changes, "file_section", None
                )
                subcategory_section.subsections.append(file_section)
            category_section.subsections.append(subcategory_section)
        sections.append(category_section)
    return sections


def _group_semantic_changes(changes: List[Change], key: str) -> List[List[Change]]:
    """Group semantic changes by a key.

    Args:
        changes: List of changes to group

    Returns:
        A list of lists of changes that share the same group.
    """
    changes_groups = []
    criteria = operator.attrgetter(f"{key}_order")

    changes = sorted(changes, key=criteria)
    for _sorted_key, changes_group in itertools.groupby(changes, key=criteria):
        changes_groups.append(list(changes_group))

    return changes_groups


def _build_newsletter_section(
    changes: List[Change],
    section_attr: str,
    subsection_attr: Optional[str],
) -> Tuple[NewsletterSection, List[Change]]:
    """Create a newsletter section from the changes.

    Ignore changes that are not part of CHANGE_TYPE_TEXT.

    Args:
        changes: The list of Change objects of the section.
        section_attr: Change attribute name that represents the section.
        subsection_attr: Change attribute name that represents the subsection.

    Returns:
        A tuple with the section object and the changes that belong to the subsection.
    """
    section = NewsletterSection(
        title=getattr(changes[0], section_attr),
        order=getattr(changes[0], f"{section_attr}_order"),
    )
    subsection_changes = []
    for change in changes:
        if subsection_attr is None or getattr(change, subsection_attr) is None:
            section.url = change.file_
            section.changes.append(change)
        else:
            subsection_changes.append(change)
    section.changes = sorted(section.changes, key=operator.attrgetter("date"))
    return section, subsection_changes


def _get_daily_newsletter_file(change: Change) -> str:
    """Return the newsletter file name of the daily feed."""
    return change.date.strftime("%Y_%m_%d.md")


def _get_weekly_newsletter_file(change: Change) -> str:
    """Return the newsletter file name of the weekly feed."""
    week_number = int(change.date.strftime("%W"))
    return f'{change.date.strftime("%Y")}_w{week_number:02}.md'


def _get_monthly_newsletter_file(change: Change) -> str:
    """Return the newsletter file name of the monthly feed."""
    return change.date.strftime("%Y_%m.md")


def _get_yearly_newsletter_file(change: Change) -> str:
    """Return the newsletter file name of the yearly feed."""
    return change.date.strftime("%Y.md")
