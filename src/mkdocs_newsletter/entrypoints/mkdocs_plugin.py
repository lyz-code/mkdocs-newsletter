"""Define the mkdocs plugin."""

import os
from typing import List

from git import Repo
from mkdocs.config.base import Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File, Files
from mkdocs.structure.nav import Navigation

from ..services.git import semantic_changes
from ..services.nav import build_nav
from ..services.newsletter import (
    add_change_categories,
    create_newsletters,
    digital_garden_changes,
    last_newsletter_changes,
)


# Class cannot subclass 'BasePlugin' (has type 'Any'). It's how the docs say you need
# to subclass it.
class Newsletter(BasePlugin):  # type: ignore
    """Define the MkDocs plugin to create newsletters."""

    def __init__(self) -> None:
        """Initialize the basic attributes.

        Args:
            repo: Git repository to analyze.
        """
        working_dir = os.getenv("NEWSLETTER_WORKING_DIR", default=os.getcwd())
        self.repo = Repo(working_dir)
        self.new_newsletters: List[File] = []

    def on_files(self, files: Files, config: Config) -> Files:
        """Load the new newsletters.

        Through the following steps:

        * Detect which were the last changes for each of the feeds.
        * Parse the changes from the git history that were done before the last changes.
        * Create the newsletter articles.

        Args:
            files: MkDocs global files collection.
            config: MkDocs global configuration object.

        Returns:
            files: MkDocs global files collection with the new newsletters.
        """
        last_published_changes = last_newsletter_changes(files)
        changes_to_publish = add_change_categories(
            semantic_changes(self.repo, last_published_changes.min()), config
        )
        changes_per_feed = digital_garden_changes(
            changes_to_publish,
            last_published_changes,
        )

        self.new_newsletters = create_newsletters(changes_per_feed, self.repo)
        for newsletter in self.new_newsletters:
            files.append(newsletter)

        return files

    def on_nav(self, nav: Navigation, config: Config, files: Files) -> Navigation:
        """Load the newsletters in the navigation menu.

        Args:
            nav: MkDocs global navigation object.
            files: MkDocs global files collection.
            config: MkDocs global configuration object.

        Returns:
            nav: MkDocs global navigation object with the newsletters.
        """
        nav = build_nav(nav, config, files)
        __import__("pdb").set_trace()  # XXX BREAKPOINT
        return nav
