"""Test the plugin entrypoint."""

import re
from datetime import datetime

import feedparser
import pytest
from dateutil import parser, tz
from git import Repo
from mkdocs.commands import build
from mkdocs.config.defaults import MkDocsConfig

from mkdocs_newsletter.version import __version__


def test_plugin_builds_newsletters(full_repo: Repo, config: MkDocsConfig) -> None:
    """
    Given:
        * A correct mkdocs directory structure.
            * A correct mkdocs.yml file.
            * Many files under `docs/`.
            * The mkdocs_newsletter plugin configured.
        * A git repository with commits.
    When: the site is built
    Then:
        * The newsletter files are created.
        * The newsletter navigation section is created.
        * The next and previos page sections are created.
    """
    build.build(config)  # act

    newsletter_path = f"{full_repo.working_dir}/site/newsletter/2021_02/index.html"
    with open(newsletter_path, "r", encoding="utf-8") as newsletter_file:
        newsletter = newsletter_file.read()
    assert "<title>February of 2021 - The Blue Book</title>" in newsletter
    assert "<h1>February of 2021</h1>" in newsletter
    assert re.search(
        r'href="../2021_03_02/"[^>]*aria-label="Previous: 2nd March 2021"', newsletter
    )
    assert re.search(
        r'href="../2021_w06/"[^>]*aria-label="Next: 6th Week of 2021"', newsletter
    )


@pytest.mark.freeze_time("2022-04-10T12:00:00")
def test_plugin_creates_daily_rss_feed(full_repo: Repo, config: MkDocsConfig) -> None:
    """
    Given:
        * A correct mkdocs directory structure.
            * A correct mkdocs.yml file.
            * Many files under `docs/`.
            * The mkdocs_newsletter plugin configured.
        * A git repository with commits.
    When: the site is built.
    Then: RSS valid daily feed is created with the expected information.
    """
    now = datetime.now(tz=tz.tzlocal())

    build.build(config)  # act

    # --------------
    # - Daily feed -
    # --------------
    rss_path = f"{full_repo.working_dir}/site/daily.xml"
    with open(rss_path, "r", encoding="utf-8") as rss_file:
        feed = feedparser.parse(rss_file.read())
    # Channel attributes
    assert feed.feed.title == "The Blue Book"
    assert feed.feed.description == "My second brain"
    assert feed.feed.link == "https://lyz-code.github.io/blue-book"
    assert feed.feed.links[1].href == "https://lyz-code.github.io/blue-book/daily.xml"
    assert parser.parse(feed.feed.published) == now
    assert feed.feed.author == "Lyz"
    assert feed.feed.ttl == "1440"
    assert feed.feed.generator == f"mkdocs-newsletter - v{__version__}"
    assert feed.feed.image.href == "https://lyz-code.github.io/blue-book/img/logo.bmp"
    # Entry attributes
    assert len(feed.entries) == 4
    assert feed.entries[0].title == "2nd March 2021"
    assert (
        feed.entries[0].link
        == "https://lyz-code.github.io/blue-book/newsletter/2021_03_02/"
    )
    assert feed.entries[0].description == (
        '<article class="md-content__inner md-typeset">\n\n'
        '<h2 id="coding">Coding</h2>\n'
        '<h3 id="tdd"><a href="https://lyz-code.github.io/blue-book/coding/tdd/">TDD'
        "</a></h3>\n"
        "<ul>\n<li>New: Define test driven development.</li>\n</ul>\n"
        '<h3 id="python">Python</h3>\n'
        '<h4 id="gitpython">'
        '<a href="https://lyz-code.github.io/blue-book/coding/python/gitpython/">'
        "GitPython</a>"
        "</h4>\n"
        "<ul>\n<li>New: Present the python library.</li>\n"
        "</ul>\n<hr />\n\n"
        "</article>"
    )
    assert parser.parse(feed.entries[0].published) == now
    assert feed.entries[0].author == "Lyz"


@pytest.mark.freeze_time("2022-04-10T12:00:00")
def test_plugin_creates_weekly_rss_feed(full_repo: Repo, config: MkDocsConfig) -> None:
    """
    Given:
        * A correct mkdocs directory structure.
            * A correct mkdocs.yml file.
            * Many files under `docs/`.
            * The mkdocs_newsletter plugin configured.
        * A git repository with commits.
    When: the site is built.
    Then: RSS valid weekly feed is created with the expected information.
    """
    now = datetime.now(tz=tz.tzlocal())

    build.build(config)  # act

    # --------------
    # - Weekly feed -
    # --------------
    rss_path = f"{full_repo.working_dir}/site/weekly.xml"
    with open(rss_path, "r", encoding="utf-8") as rss_file:
        feed = feedparser.parse(rss_file.read())
    # Channel attributes
    assert feed.feed.title == "The Blue Book"
    assert feed.feed.description == "My second brain"
    assert feed.feed.link == "https://lyz-code.github.io/blue-book"
    assert feed.feed.links[1].href == "https://lyz-code.github.io/blue-book/weekly.xml"
    # We need to do the transformation as sometimes feed.feed.published is created
    # with a different timezone
    assert parser.parse(feed.feed.published) == now
    assert feed.feed.author == "Lyz"
    assert feed.feed.ttl == "10080"
    assert feed.feed.generator == f"mkdocs-newsletter - v{__version__}"
    assert feed.feed.image.href == "https://lyz-code.github.io/blue-book/img/logo.bmp"
    # Entry attributes
    assert len(feed.entries) == 3
    assert feed.entries[0].title == "9th Week of 2021"
    assert (
        feed.entries[0].link
        == "https://lyz-code.github.io/blue-book/newsletter/2021_w09/"
    )
    assert feed.entries[0].description == (
        '<article class="md-content__inner md-typeset">\n\n'
        '<h2 id="coding">Coding</h2>\n'
        '<h3 id="tdd"><a href="https://lyz-code.github.io/blue-book/coding/tdd/">TDD'
        "</a></h3>\n"
        "<ul>\n<li>New: Define test driven development.</li>\n</ul>\n"
        '<h3 id="python">Python</h3>\n'
        '<h4 id="gitpython">'
        '<a href="https://lyz-code.github.io/blue-book/coding/python/gitpython/">'
        "GitPython</a>"
        "</h4>\n"
        "<ul>\n<li>New: Present the python library.</li>\n"
        "</ul>\n<hr />\n\n"
        "</article>"
    )
    assert parser.parse(feed.entries[0].published) == now
    assert feed.entries[0].author == "Lyz"


@pytest.mark.freeze_time("2022-04-10T12:00:00")
def test_plugin_creates_monthly_rss_feed(full_repo: Repo, config: MkDocsConfig) -> None:
    """
    Given:
        * A correct mkdocs directory structure.
            * A correct mkdocs.yml file.
            * Many files under `docs/`.
            * The mkdocs_newsletter plugin configured.
        * A git repository with commits.
    When: the site is built.
    Then: RSS valid monthly feed is created with the expected information.
    """
    now = datetime.now(tz=tz.tzlocal())

    build.build(config)  # act

    # --------------
    # - Monthly feed -
    # --------------
    rss_path = f"{full_repo.working_dir}/site/monthly.xml"
    with open(rss_path, "r", encoding="utf-8") as rss_file:
        feed = feedparser.parse(rss_file.read())
    # Channel attributes
    assert feed.feed.title == "The Blue Book"
    assert feed.feed.description == "My second brain"
    assert feed.feed.link == "https://lyz-code.github.io/blue-book"
    assert feed.feed.links[1].href == "https://lyz-code.github.io/blue-book/monthly.xml"
    # We need to do the transformation as sometimes feed.feed.published is created
    # with a different timezone
    assert parser.parse(feed.feed.published) == now
    assert feed.feed.author == "Lyz"
    assert feed.feed.ttl == "43200"
    assert feed.feed.generator == f"mkdocs-newsletter - v{__version__}"
    assert feed.feed.image.href == "https://lyz-code.github.io/blue-book/img/logo.bmp"
    # Entry attributes
    assert len(feed.entries) == 2
    assert feed.entries[0].title == "March of 2021"
    assert (
        feed.entries[0].link
        == "https://lyz-code.github.io/blue-book/newsletter/2021_03/"
    )
    assert feed.entries[0].description == (
        '<article class="md-content__inner md-typeset">\n\n'
        '<h2 id="coding">Coding</h2>\n'
        '<h3 id="tdd"><a href="https://lyz-code.github.io/blue-book/coding/tdd/">TDD'
        "</a></h3>\n"
        "<ul>\n<li>New: Define test driven development.</li>\n</ul>\n"
        '<h3 id="python">Python</h3>\n'
        '<h4 id="gitpython">'
        '<a href="https://lyz-code.github.io/blue-book/coding/python/gitpython/">'
        "GitPython</a>"
        "</h4>\n"
        "<ul>\n<li>New: Present the python library.</li>\n"
        "</ul>\n<hr />\n\n"
        "</article>"
    )
    assert parser.parse(feed.entries[0].published) == now
    assert feed.entries[0].author == "Lyz"


@pytest.mark.freeze_time("2022-04-10T12:00:00")
def test_plugin_creates_yearly_rss_feed(full_repo: Repo, config: MkDocsConfig) -> None:
    """
    Given:
        * A correct mkdocs directory structure.
            * A correct mkdocs.yml file.
            * Many files under `docs/`.
            * The mkdocs_newsletter plugin configured.
        * A git repository with commits.
    When: the site is built.
    Then: RSS valid yearly feed is created with the expected information.
    """
    now = datetime.now(tz=tz.tzlocal())

    build.build(config)  # act

    # --------------
    # - Yearly feed -
    # --------------
    rss_path = f"{full_repo.working_dir}/site/yearly.xml"
    with open(rss_path, "r", encoding="utf-8") as rss_file:
        feed = feedparser.parse(rss_file.read())
    # Channel attributes
    assert feed.feed.title == "The Blue Book"
    assert feed.feed.description == "My second brain"
    assert feed.feed.link == "https://lyz-code.github.io/blue-book"
    assert feed.feed.links[1].href == "https://lyz-code.github.io/blue-book/yearly.xml"
    # We need to do the transformation as sometimes feed.feed.published is created
    # with a different timezone
    assert parser.parse(feed.feed.published) == now
    assert feed.feed.author == "Lyz"
    assert feed.feed.ttl == "525600"
    assert feed.feed.generator == f"mkdocs-newsletter - v{__version__}"
    assert feed.feed.image.href == "https://lyz-code.github.io/blue-book/img/logo.bmp"
    # Entry attributes
    assert len(feed.entries) == 1
    assert feed.entries[0].title == "2021"
    assert (
        feed.entries[0].link == "https://lyz-code.github.io/blue-book/newsletter/2021/"
    )
    assert feed.entries[0].description == (
        '<article class="md-content__inner md-typeset">\n\n'
        '<h2 id="devops"><a href="https://lyz-code.github.io/blue-book/devops/devops/">'
        "DevOps</a></h2>\n"
        "<ul>\n<li>\n<p>New: Define DevOps.</p>\n"
        '<p><a href="https://en.wikipedia.org/wiki/DevOps">DevOps</a> is a set of '
        "practices that\ncombines software development (Dev) and "
        "information-technology operations\n(Ops) which aims to shorten the systems "
        "development life cycle and "
        "provide\ncontinuous delivery with high software quality.</p>\n<p>One of the "
        "most important goals of the DevOps initiative is to break the\nsilos between "
        "the developers and the sysadmins, that lead to ill feelings\nand "
        'unproductivity.</p>\n</li>\n</ul>\n<h3 id="infrastructure-as-code">'
        'Infrastructure as Code</h3>\n<h4 id="helm">'
        '<a href="https://lyz-code.github.io/blue-book/devops/helm/helm/">'
        "Helm</a></h4>\n<ul>\n<li>\n<p>New: Introduce Helm the Kubernetes "
        'package manager.</p>\n<p><a href="https://helm.sh/">Helm</a> is the package '
        "manager for Kubernetes. Through\ncharts it helps you define, install and "
        "upgrade even the most complex\nKubernetes applications.</p>\n</li>\n</ul>\n"
        '<h2 id="coding">Coding</h2>\n'
        '<h3 id="tdd"><a href="https://lyz-code.github.io/blue-book/coding/tdd/">TDD'
        "</a></h3>\n"
        "<ul>\n<li>New: Define test driven development.</li>\n</ul>\n"
        '<h3 id="python">Python</h3>\n'
        '<h4 id="gitpython">'
        '<a href="https://lyz-code.github.io/blue-book/coding/python/gitpython/">'
        "GitPython</a></h4>\n"
        "<ul>\n<li>New: Present the python library.</li>\n</ul>\n"
        '<h2 id="other">Other</h2>\n'
        "<ul>\n<li>New: Add funny emojis.</li>\n"
        "<li>New: Add ash, birch and beech information.</li>\n"
        "</ul>\n<hr />\n\n"
        "</article>"
    )
    assert parser.parse(feed.entries[0].published) == now
    assert feed.entries[0].author == "Lyz"


@pytest.mark.freeze_time("2022-04-10T12:00:00")
def test_plugin_creates_landing_page(full_repo: Repo, config: MkDocsConfig) -> None:
    """
    Given:
        * A correct mkdocs directory structure.
            * A correct mkdocs.yml file.
            * Many files under `docs/`.
            * The mkdocs_newsletter plugin configured.
        * A git repository with commits.
    When: the site is built.
    Then: The newsletter landing page is built
    """
    build.build(config)  # act

    landing_path = (
        f"{full_repo.working_dir}/site/newsletter/0_newsletter_index/index.html"
    )
    with open(landing_path, "r", encoding="utf-8") as landing_file:
        landing_page = landing_file.read()
    assert "<title>Newsletters - The Blue Book</title>" in landing_page
    assert (
        "If you want to follow the meaningful changes of this site, you can either"
        in landing_page
    )
    assert (
        '<a href="https://lyz-code.github.io/blue-book/daily.xml">Daily</a>'
        in landing_page
    )
    assert "<h1>Newsletters</h1>" in landing_page
    assert re.search(
        r'href="../../emojis/"[^>]*aria-label="Previous: Emojis"', landing_page
    )
    assert re.search(r'href="../2021/"[^>]*aria-label="Next: 2021"', landing_page)


def test_build_rss_feed_without_logo(config: MkDocsConfig, full_repo: Repo) -> None:
    """
    Given: A Config site without logo.
    When: The site is built
    Then: No error is shown and the site builds correctly.
    """
    # W0212: access to a protected attribute of a class, it's just to simulate a site
    # without logo.
    config["theme"]._vars.pop("logo")  # noqa: W0212

    build.build(config)  # act

    rss_path = f"{full_repo.working_dir}/site/yearly.xml"
    with open(rss_path, "r", encoding="utf-8") as rss_file:
        feed = feedparser.parse(rss_file.read())
    # Channel attributes
    assert feed.feed.title == "The Blue Book"
    assert feed.feed.description == "My second brain"
