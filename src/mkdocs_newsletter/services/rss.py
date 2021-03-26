"""Define the RSS management services."""

import datetime
import os
import re
from contextlib import suppress
from typing import List, Optional

from bs4 import BeautifulSoup
from jinja2 import Environment, PackageLoader, select_autoescape
from mkdocs.config.base import Config

from ..model import Feed, FeedEntry, NewsletterType
from ..version import __version__
from .newsletter import _list_newsletters

TTL = {
    "daily": 1440,
    "weekly": 10080,
    "monthly": 43200,
    "yearly": 525600,
}


def create_rss(config: Config, working_dir: str) -> None:
    """Create RSS feed with the newsletters of a period."""
    feed_types = [type_.value for type_ in NewsletterType]
    for feed_type in feed_types:
        feed = build_rss_feed(config, working_dir, feed_type)

        env = Environment(
            loader=PackageLoader("mkdocs_newsletter", "templates"),
            autoescape=select_autoescape(["html", "xml"]),
        )
        template = env.get_template("rss.xml.j2")

        feed_path = os.path.join(config["site_dir"], f"{feed_type}.xml")
        feed_content = template.render(feed=feed)
        with open(feed_path, "+w") as feed_file:
            feed_file.write(feed_content)


def build_rss_feed(config: Config, working_dir: str, type_: str) -> Feed:
    """Create the RSS feed data from the content.

    Args:
        config: MkDocs config object.
        type_: type of feed, one of: daily, weekly, monthly or yearly.

    Returns:
        Feed object with the data
    """
    site_url = config["site_url"]

    try:
        logo_url: Optional[str] = f"{site_url}/{config['theme']['logo']}"
    except KeyError:
        logo_url = None

    author = config.get("site_author", None)

    entries = _build_rss_entries(config, working_dir, type_, author)

    try:
        published = max(entries).published
    except ValueError:
        published = datetime.datetime.now()

    return Feed(
        ttl=TTL[type_],
        generator=f"mkdocs-newsletter - v{__version__}",
        title=config.get("site_name", None),
        link=site_url,
        rss_link=f"{site_url}/{type_}.xml",
        logo=logo_url,
        description=config.get("site_description", None),
        author=author,
        published=published,
        entries=entries,
    )


def _build_rss_entries(
    config: Config,
    working_dir: str,
    type_: str,
    author: Optional[str],
) -> List[FeedEntry]:
    """Create the RSS feed entries for a feed type.

    Args:
        config: MkDocs config object.
        type_: type of feed, one of: daily, weekly, monthly or yearly.
        working_dir: Mkdocs root directory.
        author: author name.

    Returns:
        List of FeedEntry objects with the data.
    """
    entries = []

    newsletter_dir = os.path.join(
        working_dir, f'{config.get("site_dir", "site")}/newsletter'
    )

    newsletters = _list_newsletters(os.path.join(working_dir, "docs/newsletter"))

    for newsletter in getattr(newsletters, type_):
        with open(
            f"{newsletter_dir}/{newsletter.basename}/index.html", "r"
        ) as newsletter_file:
            html = BeautifulSoup(newsletter_file, "html.parser")

        try:
            published = html.findAll("span", {"class": "timeago"})[0]["datetime"]
        except IndexError:
            published = newsletter.date.isoformat()

        # Clean the source code

        # Remove the h1 as it's already in the title
        title = html.article.h1.text
        html.article.h1.extract()

        # Remove the Last updated: line
        with suppress(AttributeError):
            html.article.div.extract()

        # Remove the permalinks
        for permalink in html.article.findAll("a", {"class": "headerlink"}):
            permalink.extract()

        description = re.sub(
            r'<a href="../../', f'<a href="{config["site_url"]}/', str(html.article)
        )

        entry = FeedEntry(
            title=title,
            link=f"{config['site_url']}/newsletter/{newsletter.basename}/",
            published=published,
            description=description,
            author=author,
        )
        entries.append(entry)

        if len(entries) > 15:
            break

    return entries
