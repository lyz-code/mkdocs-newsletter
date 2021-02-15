"""Tests the service layer.

The time freezes are meant to simulate the special state of the fake git repository
defined in the Given: statement of the test docstring. You can check it in the repo
fixture definition at conftest.py.
"""

import datetime
import textwrap

import pytest
from dateutil import tz
from git import Actor, Repo

from mkdocs_newsletter import Change, services

author = Actor("An author", "author@example.com")
committer = Actor("A committer", "committer@example.com")


@pytest.mark.freeze_time("2021-02-01T12:00:00")
def test_changes_dont_extract_commits_that_dont_comply_with_syntax(repo: Repo) -> None:
    """
    Given: A mkdocs git repo with a change whose message is not compliant with the
        commit message guidelines.
    When: changes is called
    Then: No Change is returned
    """
    commit_date = datetime.datetime(2021, 2, 1, tzinfo=tz.tzlocal())
    repo.index.add(["mkdocs.yml"])
    repo.index.commit(
        "Initial skeleton",
        author=author,
        committer=committer,
        author_date=commit_date,
        commit_date=commit_date,
    )

    result = services.semantic_changes(repo)

    assert len(result) == 0


@pytest.mark.freeze_time("2021-02-02T12:00:00")
def test_changes_extracts_commits_that_dont_specify_scope(repo: Repo) -> None:
    """
    Given: A mkdocs git repo with a change whose message follows the correct syntax
        but doesn't specify the scope of the change.
    When: changes is called
    Then: The expected Change is returned
    """
    commit_date = datetime.datetime(2021, 2, 2, tzinfo=tz.tzlocal())
    repo.index.add(["docs/emojis.md"])
    repo.index.commit(
        "feat: add funny emojis",
        author=author,
        committer=committer,
        author_date=commit_date,
        commit_date=commit_date,
    )
    expected_change = Change(
        date=commit_date, summary="Add funny emojis.", type_="feature", scope=None,
    )

    result = services.semantic_changes(repo)

    assert result == [expected_change]


@pytest.mark.freeze_time("2021-02-05T12:00:00")
def test_changes_extracts_commits_with_multiple_changes(repo: Repo) -> None:
    """
    Given: A mkdocs git repo with a change whose message follows the correct syntax,
        contains two semantic changes with scope and description.
    When: changes is called.
    Then: The two expected Changes are returned.
    """
    commit_date = datetime.datetime(2021, 2, 5, tzinfo=tz.tzlocal())
    repo.index.add(["docs/devops/helm/helm.md", "docs/devops/devops.md"])
    repo.index.commit(
        textwrap.dedent(
            """\
            feat(helm): introduce Helm the Kubernetes package manager

            [Helm](https://helm.sh/) is the package manager for Kubernetes. Through
            charts it helps you define, install and upgrade even the most complex
            Kubernetes applications.

            feat(devops): define DevOps

            [DevOps](https://en.wikipedia.org/wiki/DevOps) is a set of practices that
            combines software development (Dev) and information-technology operations
            (Ops) which aims to shorten the systems development life cycle and provide
            continuous delivery with high software quality.

            One of the most important goals of the DevOps initiative is to break the
            silos between the developers and the sysadmins, that lead to ill feelings
            and unproductivity."""
        ),
        author=author,
        committer=committer,
        author_date=commit_date,
        commit_date=commit_date,
    )
    expected_changes = [
        Change(
            date=commit_date,
            summary="Introduce Helm the Kubernetes package manager.",
            description=(
                "[Helm](https://helm.sh/) is the package manager for Kubernetes. "
                "Through charts it helps you define, install and upgrade even the most "
                "complex Kubernetes applications."
            ),
            type_="feature",
            scope="helm",
        ),
        Change(
            date=commit_date,
            summary="Define DevOps.",
            description=(
                "[DevOps](https://en.wikipedia.org/wiki/DevOps) is a set of practices "
                "that combines software development (Dev) and information-technology "
                "operations (Ops) which aims to shorten the systems development life "
                "cycle and provide continuous delivery with high software quality."
                ""
                "One of the most important goals of the DevOps initiative is to break "
                "the silos between the developers and the sysadmins, that lead to ill "
                "feelings and unproductivity."
            ),
            type_="feature",
            scope="devops",
        ),
    ]

    result = services.semantic_changes(repo)

    assert result == expected_changes


@pytest.mark.freeze_time("2021-02-10T12:00:00")
def test_digital_garden_changes_to_publish_selects_last_week_changes(
    repo: Repo,
) -> None:
    """
    Given: A mkdocs git repo with changes done in the last and current weeks.
    When: changes_to_publish is called.
    Then: Only last week changes are selected to be published for the weekly feed.
    """
    last_week_commit_date = datetime.datetime(2021, 2, 2, tzinfo=tz.tzlocal())
    repo.index.add(["docs/emojis.md"])
    repo.index.commit(
        "feat: add funny emojis",
        author=author,
        committer=committer,
        author_date=last_week_commit_date,
        commit_date=last_week_commit_date,
    )
    this_week_commit_date = datetime.datetime(2021, 2, 8, tzinfo=tz.tzlocal())
    repo.index.add(["docs/botany/trees.md"])
    repo.index.commit(
        "feat(botany): add ash, birch and beech information",
        author=author,
        committer=committer,
        author_date=this_week_commit_date,
        commit_date=this_week_commit_date,
    )
    last_week_change = Change(
        date=last_week_commit_date,
        summary="Add funny emojis.",
        type_="feature",
        scope=None,
    )
    this_week_change = Change(
        date=this_week_commit_date,
        summary="Add ash, birch and beech information.",
        type_="feature",
        scope="botany",
    )

    result = services.digital_garden_changes(repo)

    assert last_week_change in result.weekly
    assert this_week_change not in result.weekly


@pytest.mark.freeze_time("2021-02-10T12:00:00")
def test_digital_garden_changes_to_publish_selects_last_month_changes(
    repo: Repo,
) -> None:
    """
    Given: A mkdocs git repo with changes done in the last and the current months.
    When: changes_to_publish is called.
    Then: Only last month changes are selected to be published for the yearly feed.
    """
    last_month_commit_date = datetime.datetime(2021, 1, 2, tzinfo=tz.tzlocal())
    repo.index.add(["docs/emojis.md"])
    repo.index.commit(
        "feat: add funny emojis",
        author=author,
        committer=committer,
        author_date=last_month_commit_date,
        commit_date=last_month_commit_date,
    )
    this_month_commit_date = datetime.datetime(2021, 2, 8, tzinfo=tz.tzlocal())
    repo.index.add(["docs/botany/trees.md"])
    repo.index.commit(
        "feat(botany): add ash, birch and beech information",
        author=author,
        committer=committer,
        author_date=this_month_commit_date,
        commit_date=this_month_commit_date,
    )
    last_month_change = Change(
        date=last_month_commit_date,
        summary="Add funny emojis.",
        type_="feature",
        scope=None,
    )
    this_month_change = Change(
        date=this_month_commit_date,
        summary="Add ash, birch and beech information.",
        type_="feature",
        scope="botany",
    )

    result = services.digital_garden_changes(repo)

    assert last_month_change in result.monthly
    assert this_month_change not in result.monthly


@pytest.mark.freeze_time("2021-02-10T12:00:00")
def test_digital_garden_changes_to_publish_selects_last_year_changes(
    repo: Repo,
) -> None:
    """
    Given: A mkdocs git repo with changes done in the last and the current years.
    When: changes_to_publish is called.
    Then: Only last year changes are selected to be published for the yearly feed.
    """
    last_year_commit_date = datetime.datetime(2020, 1, 2, tzinfo=tz.tzlocal())
    repo.index.add(["docs/emojis.md"])
    repo.index.commit(
        "feat: add funny emojis",
        author=author,
        committer=committer,
        author_date=last_year_commit_date,
        commit_date=last_year_commit_date,
    )
    this_year_commit_date = datetime.datetime(2021, 2, 8, tzinfo=tz.tzlocal())
    repo.index.add(["docs/botany/trees.md"])
    repo.index.commit(
        "feat(botany): add ash, birch and beech information",
        author=author,
        committer=committer,
        author_date=this_year_commit_date,
        commit_date=this_year_commit_date,
    )
    last_year_change = Change(
        date=last_year_commit_date,
        summary="Add funny emojis.",
        type_="feature",
        scope=None,
    )
    this_year_change = Change(
        date=this_year_commit_date,
        summary="Add ash, birch and beech information.",
        type_="feature",
        scope="botany",
    )

    result = services.digital_garden_changes(repo)

    assert last_year_change in result.yearly
    assert this_year_change not in result.yearly
