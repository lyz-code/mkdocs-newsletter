"""Define the mkdocs plugin."""

import os

from git import Repo
from mkdocs.config.base import Config
from mkdocs.plugins import BasePlugin

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

        Attributes:
            repo: Git repository to analyze.
        """
        self.working_dir = os.getenv("NEWSLETTER_WORKING_DIR", default=os.getcwd())
        self.repo = Repo(self.working_dir)

    def on_config(self, config: Config) -> Config:
        """Create the new newsletters and load them in the navigation.

        Through the following steps:

        * Detect which were the last changes for each of the feeds.
        * Parse the changes from the git history that were done before the last
            changes.
        * Create the newsletter articles.
        * Update the navigation.

        Args:
            config: MkDocs global configuration object.

        Returns:
            config: MkDocs config object with the new newsletters in the Newsletter
                section.
        """
        newsletter_dir = f"{self.working_dir}/docs/newsletter"
        if not os.path.exists(newsletter_dir):
            os.makedirs(newsletter_dir)
        last_published_changes = last_newsletter_changes(newsletter_dir)
        changes_to_publish = add_change_categories(
            semantic_changes(self.repo, last_published_changes.min()), config
        )
        changes_per_feed = digital_garden_changes(
            changes_to_publish,
            last_published_changes,
        )

        create_newsletters(changes_per_feed, self.repo)

        config = build_nav(config, newsletter_dir)

        return config
