"""Gather all the orchestration functionality required by the program to work.

Classes and functions that connect the different domain model objects with the adapters
and handlers to achieve the program's purpose.
"""

import datetime
import re
from contextlib import suppress
from typing import List, Optional, Tuple

from dateutil import tz
from git import Commit, Repo  # type: ignore

from ..model import Change

TYPES = {
    "feat": "feature",
    "fix": "fix",
    "test": "test",
    "docs": "documentation",
    "style": "style",
    "refactor": "refactor",
    "build": "build",
    "ci": "ci",
    "perf": "performance",
    "chore": "chore",
}


def semantic_changes(
    repo: Repo, min_date: Optional[datetime.datetime] = None
) -> List[Change]:
    """Extract meaningful changes from a git repository.

    Args:
        repo: Git repository to analyze.

    Returns:
        changes: List of Change objects.
    """
    now = datetime.datetime.now(tz=tz.tzlocal())
    if min_date is None:
        min_date = datetime.datetime(1800, 1, 1, tzinfo=tz.tzlocal())

    commits = [
        commit
        for commit in repo.iter_commits(rev=repo.head.reference)
        if commit.authored_datetime < now and commit.authored_datetime > min_date
    ]

    return commits_to_changes(commits)


def commits_to_changes(commits: List[Commit]) -> List[Change]:
    """Extract the semantic changes from a list of commits.

    Args:
        commits: List of commits to parse.

    Returns:
        changes: List of semantic changes.
    """
    changes = []

    for commit in commits:
        with suppress(ValueError):
            changes += commit_to_changes(commit)

    return changes


def commit_to_changes(commit: Commit) -> List[Change]:
    """Extract the semantic changes from a commit.

    Args:
        commit: Commit to parse.

    Returns:
        changes: List of semantic changes.
    """
    changes: List[Change] = []
    remaining = commit.message

    while remaining is not None:
        try:
            change, remaining = _parse_change(remaining, commit.authored_date)
        except ValueError:
            return changes
        changes.append(change)
    return changes


def _parse_change(
    message: str, date: datetime.datetime
) -> Tuple[Change, Optional[str]]:
    """Extract a semantic change from a commit message.

    Args:
        message: Commit message to parse.

    Returns:
        changes: List of semantic changes.
        remaining: The rest of the commit message.

    Raises:
        ValueError: when the commit message doesn't follow the commit guidelines.
    """
    commit_regexp = re.compile(
        rf"(?P<type>{'|'.join(TYPES.keys())})"
        r"(?:\((?P<scope>[^\)]+)\))?"
        r": (?P<summary>[^\n\n]+)"
        r"(:?\n\n(?P<text>.+))?",
        re.DOTALL,
    )

    commit_match = commit_regexp.match(message)
    if not commit_match:
        raise ValueError(f"Unable to parse the given commit message: {message}")

    change = Change(
        date=date,
        summary=_clean_summary(commit_match.group("summary")),
        type_=TYPES[commit_match.group("type")],
        scope=commit_match.group("scope"),
    )

    remaining = commit_match.group("text")

    description_lines: List[str] = []
    while remaining not in [None, ""] and not commit_regexp.match(remaining):
        remaining_lines = remaining.split("\n\n")
        description_lines.append(remaining_lines.pop(0))
        remaining = "\n\n".join(remaining_lines)

    if len(description_lines) > 0:
        change.message = "\n\n".join(description_lines)

    return change, remaining


def _clean_summary(summary: str) -> str:
    """Clean the commit summary line.

    Ensure that:

    * The first character of the first word is in upper caps.
    * The line ends with a dot.
    """
    summary = summary[0].upper() + summary[1:]
    if summary[-1] != ".":
        summary += "."

    return summary
