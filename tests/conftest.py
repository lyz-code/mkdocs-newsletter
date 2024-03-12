"""Store the classes and fixtures used throughout the tests."""

import datetime
import os
import shutil
import textwrap
from pathlib import Path

import pytest
from dateutil import tz
from git import Actor, Repo
from mkdocs.config.base import load_config
from mkdocs.config.defaults import MkDocsConfig


@pytest.fixture(name="repo")
def repo_(tmp_path: Path) -> Repo:
    """Initialize an empty git repository with fake unstaged data.

    Args:
        tmp_path: Pytest fixture that creates a temporal directory
    """
    # Copy the content from `tests/assets/test_data`.
    repo_path = tmp_path / "test_data"
    os.environ["NEWSLETTER_WORKING_DIR"] = str(repo_path)
    shutil.copytree("tests/assets/test_data", repo_path)

    return Repo.init(repo_path)


@pytest.fixture(name="full_repo")
def full_repo_(repo: Repo) -> Repo:
    """Create a git repository with fake data and history.

    Args:
        repo: an initialized Repo
    """
    index = repo.index
    author = Actor("An author", "author@example.com")
    committer = Actor("A committer", "committer@example.com")

    # ---------------------------
    # Creates a fake git history
    # ---------------------------

    #    February 2021
    # Mo Tu We Th Fr Sa Su
    #  1  2  3  4  5  6  7
    #  8  9 10 11 12 13 14
    # 15 16 17 18 19 20 21
    # 22 23 24 25 26 27 28

    # Commit that doesn't follow the semantic versioning syntax (will be ignored).
    commit_date = datetime.datetime(2021, 2, 1, 12, tzinfo=tz.tzlocal())
    index.add(["mkdocs.yml"])
    index.commit(
        "Initial skeleton",
        author=author,
        committer=committer,
        author_date=commit_date,
        commit_date=commit_date,
    )

    # Single change commit that follows the correct syntax without specifying the file
    # it affects
    commit_date = datetime.datetime(2021, 2, 2, 12, tzinfo=tz.tzlocal())
    index.add(["docs/emojis.md"])
    index.commit(
        "feat: add funny emojis",
        author=author,
        committer=committer,
        author_date=commit_date,
        commit_date=commit_date,
    )

    # Multi change commit that follows the correct syntax specifying the files
    # it affects and a short description of each change.
    commit_date = datetime.datetime(2021, 2, 5, 12, tzinfo=tz.tzlocal())
    index.add(["docs/devops/helm/helm.md", "docs/devops/devops.md"])
    index.commit(
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

    # Single change commit that corrects the style of a file.
    with open(
        os.path.join(str(repo.working_dir), "docs/emojis.md"), "a", encoding="utf-8"
    ) as file_object:
        # Simulate the change by appending a string at the end of the file.
        file_object.write("correct link")
    commit_date = datetime.datetime(2021, 2, 6, 12, tzinfo=tz.tzlocal())
    index.add(["docs/emojis.md"])
    index.commit(
        "style(devops): correct link",
        author=author,
        committer=committer,
        author_date=commit_date,
        commit_date=commit_date,
    )

    # Single chore change.
    commit_date = datetime.datetime(2021, 2, 7, 12, tzinfo=tz.tzlocal())
    index.add(["requirements.txt"])
    index.commit(
        "chore: update requirements",
        author=author,
        committer=committer,
        author_date=commit_date,
        commit_date=commit_date,
    )

    # Another single change commit done the next week.
    commit_date = datetime.datetime(2021, 2, 8, 12, tzinfo=tz.tzlocal())
    index.add(["docs/botany/trees.md"])
    index.commit(
        "feat(botany): add ash, birch and beech information",
        author=author,
        committer=committer,
        author_date=commit_date,
        commit_date=commit_date,
    )

    # Another multi change commit done the next month.
    commit_date = datetime.datetime(2021, 3, 2, 12, tzinfo=tz.tzlocal())
    index.add(["docs/coding/tdd.md", "docs/coding/python/gitpython.md"])
    index.commit(
        textwrap.dedent(
            """\
            feat(tdd): define test driven development

            feat(gitpython): present the python library"""
        ),
        author=author,
        committer=committer,
        author_date=commit_date,
        commit_date=commit_date,
    )

    return repo


@pytest.fixture(name="config")
def config_(full_repo: Repo) -> MkDocsConfig:
    """Load the mkdocs configuration."""
    mkdocs_config = load_config(os.path.join(str(full_repo.working_dir), "mkdocs.yml"))
    mkdocs_config["site_dir"] = os.path.join(str(full_repo.working_dir), "site")
    return mkdocs_config
