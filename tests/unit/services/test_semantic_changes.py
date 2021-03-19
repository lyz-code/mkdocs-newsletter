"""Tests the extraction of semantic changes from the git history.

The time freezes are meant to simulate the special state of the fake git repository
defined in the Given: statement of the test docstring. You can check it in the repo
fixture definition at conftest.py.
"""

import datetime
import textwrap
from textwrap import dedent

import pytest
from dateutil import tz
from git import Actor, Repo

from mkdocs_newsletter import Change, semantic_changes

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

    result = semantic_changes(repo)

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
        date=commit_date,
        summary="Add funny emojis.",
        type_="feature",
        scope=None,
    )

    result = semantic_changes(repo)

    assert result == [expected_change]


@pytest.mark.freeze_time("2021-02-05T12:00:00")
def test_changes_extracts_commits_with_multiple_changes(repo: Repo) -> None:
    """
    Given: A mkdocs git repo with a change whose message follows the correct syntax,
        contains two semantic changes with scope and description.
    When: changes is called.
    Then: The two expected Changes are returned, where the message respects the
        line breaks.
    """
    commit_date = datetime.datetime(2021, 2, 5, tzinfo=tz.tzlocal())
    repo.index.add(["docs/devops/helm/helm.md", "docs/devops/devops.md"])
    repo.index.commit(
        textwrap.dedent(
            """\
            feat(helm): introduce Helm the Kubernetes package manager

            [Helm](https://helm.sh/) is the package manager for Kubernetes.
            Through charts it helps you define, install and upgrade even the most
            complex Kubernetes applications.

            feat(devops): define DevOps

            [DevOps](https://en.wikipedia.org/wiki/DevOps) is a set of practices
            that combines software development (Dev) and information-technology
            operations (Ops) which aims to shorten the systems development life
            cycle and provide continuous delivery with high software quality.

            One of the most important goals of the DevOps initiative is to break
            the silos between the developers and the sysadmins, that lead to ill
            feelings and unproductivity."""
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
            message=dedent(
                """\
                [Helm](https://helm.sh/) is the package manager for Kubernetes.
                Through charts it helps you define, install and upgrade even the most
                complex Kubernetes applications."""
            ),
            type_="feature",
            scope="helm",
        ),
        Change(
            date=commit_date,
            summary="Define DevOps.",
            message=dedent(
                """\
                [DevOps](https://en.wikipedia.org/wiki/DevOps) is a set of practices
                that combines software development (Dev) and information-technology
                operations (Ops) which aims to shorten the systems development life
                cycle and provide continuous delivery with high software quality.

                One of the most important goals of the DevOps initiative is to break
                the silos between the developers and the sysadmins, that lead to ill
                feelings and unproductivity."""
            ),
            type_="feature",
            scope="devops",
        ),
    ]

    result = semantic_changes(repo)

    assert result == expected_changes


@pytest.mark.freeze_time("2021-02-05T12:00:00")
def test_changes_dont_extract_commits_older_than_min_date(repo: Repo) -> None:
    """
    Given: A mkdocs git repo with a change older and other younger than the min_date.
    When: changes is called
    Then: Only the younger Change is returned
    """
    repo.index.add(["mkdocs.yml"])
    commit_date = datetime.datetime(2021, 2, 1, tzinfo=tz.tzlocal())
    repo.index.commit(
        "feat: Old commit",
        author=author,
        committer=committer,
        author_date=commit_date,
        commit_date=commit_date,
    )
    commit_date = datetime.datetime(2021, 2, 3, tzinfo=tz.tzlocal())
    repo.index.commit(
        "feat: New commit",
        author=author,
        committer=committer,
        author_date=commit_date,
        commit_date=commit_date,
    )

    result = semantic_changes(repo, datetime.datetime(2021, 2, 2, tzinfo=tz.tzlocal()))

    assert len(result) == 1
    assert result[0].summary == "New commit."


@pytest.mark.freeze_time("2021-02-02T12:00:00")
def test_changes_extracts_commits_with_scope_with_spaced_subsection(repo: Repo) -> None:
    """
    Given: A mkdocs git repo with a change whose message follows the correct syntax
        and specifies the scope of the change with subsection with spaces in it.
    When: changes is called
    Then: The expected Change is returned
    """
    commit_date = datetime.datetime(2021, 2, 2, tzinfo=tz.tzlocal())
    repo.index.add(["docs/emojis.md"])
    repo.index.commit(
        "feat(emojis#Spaced subsection): add funny emojis",
        author=author,
        committer=committer,
        author_date=commit_date,
        commit_date=commit_date,
    )
    expected_change = Change(
        date=commit_date,
        summary="Add funny emojis.",
        type_="feature",
        scope="emojis#Spaced subsection",
    )

    result = semantic_changes(repo)

    assert result == [expected_change]
