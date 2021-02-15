"""Gather all the orchestration functionality required by the program to work.

Classes and functions that connect the different domain model objects with the adapters
and handlers to achieve the program's purpose.
"""

import datetime
from typing import List, Tuple

from dateutil import tz
from git import Commit, Repo
from semantic_release.errors import UnknownCommitMessageStyleError
from semantic_release.history.parser_angular import parse_commit_message
from semantic_release.history.parser_helpers import ParsedCommit

from .model import Change, DigitalGardenChanges


def digital_garden_changes(repo: Repo) -> DigitalGardenChanges:
    """Extract the changes that need to be published for digital_garden repositories.

    For a change to be published it needs to:

    * Be made before last Monday.
    * Be made after the last meaningful tag.

    Args:
        repo: Git repository to analyze.

    Returns:
        changes: List of Change objects to publish.
    """
    now = datetime.datetime.now(tz.tzlocal())
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    last_first_weekday = today - datetime.timedelta(days=now.weekday())
    last_first_monthday = today.replace(day=1)
    last_first_yearday = today.replace(day=1, month=1)

    changes = semantic_changes(repo)

    return DigitalGardenChanges(
        weekly=[change for change in changes if change.date < last_first_weekday],
        monthly=[change for change in changes if change.date < last_first_monthday],
        yearly=[change for change in changes if change.date < last_first_yearday],
    )


def semantic_changes(repo: Repo) -> List[Change]:
    """Extract meaningful changes from a git repository.

    Args:
        repo: Git repository to analyze.

    Returns:
        changes: List of Change objects.
    """
    commits = [
        commit
        for commit in repo.iter_commits(rev=repo.head.reference)
        if commit.authored_datetime < datetime.datetime.now(tz=tz.tzlocal())
    ]
    changes = commits_to_changes(commits)

    return changes


def commits_to_changes(commits: List[Commit]) -> List[Change]:
    """Extract the semantic changes from a list of commits.

    Args:
        commits: List of commits to parse.

    Returns:
        changes: List of semantic changes.
    """
    changes = []

    for commit in commits:
        changes += commit_to_changes(commit)

    return changes


def commit_to_changes(commit: Commit) -> List[Change]:
    """Extract the semantic changes from a commit.

    Args:
        commit: Commits to parse.

    Returns:
        changes: List of semantic changes.
    """
    changes: List[Change] = []

    try:
        parsed_commit = parse_commit_message(commit.message)
    except UnknownCommitMessageStyleError:
        return changes

    while True:
        try:
            parsed_commit, new_parsed_commit = _extract_changes_from_description(
                parsed_commit
            )
            changes.append(
                Change(
                    date=commit.authored_datetime,
                    summary=_clean_summary(parsed_commit),
                    type_=parsed_commit.type,
                    scope=parsed_commit.scope,
                )
            )
            parsed_commit = new_parsed_commit
        except StopIteration:
            break
    changes.append(
        Change(
            date=commit.authored_datetime,
            summary=_clean_summary(parsed_commit),
            type_=parsed_commit.type,
            scope=parsed_commit.scope,
        )
    )

    return changes


def _extract_changes_from_description(
    parsed_commit: ParsedCommit,
) -> Tuple[ParsedCommit, ParsedCommit]:
    """Extract changes from the parsed_commit description.

    parse_commit_message only extracts one change per commit message. If there
    are more than one, they get added as part of the description.

    Args:
        parsed_commit: ParsedCommit object to clean

    Returns:
        parsed_commit: Original parsed_commit with the clean description.
        new_parsed_commit: New ParsedCommit extracted from the original's description.

    Raises:
        StopIteration: If there is no other semantic change in the description.
    """
    start = 1
    while True:
        try:
            remaining = parsed_commit.descriptions[start:]
            if len(remaining) == 0:
                raise StopIteration

            new_parsed_commit = parse_commit_message("\n\n".join(remaining))
            # Replace the description attribute, as it's a NamedTuple, we need to create
            # a new one -.-
            parsed_commit = ParsedCommit(
                descriptions=parsed_commit.descriptions[:start],
                bump=parsed_commit.bump,
                type=parsed_commit.type,
                scope=parsed_commit.scope,
                breaking_descriptions=parsed_commit.breaking_descriptions,
            )
            return parsed_commit, new_parsed_commit
        except UnknownCommitMessageStyleError:
            start += 1


def _clean_summary(parsed_commit: ParsedCommit) -> str:
    """Clean the commit summary line.

    Ensure that:

    * The first character of the first word is in upper caps.
    * The line ends with a dot.
    """
    summary = parsed_commit.descriptions[0]
    summary = summary[0].upper() + summary[1:]
    if summary[-1] != ".":
        summary += "."

    return summary
