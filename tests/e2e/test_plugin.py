"""Test the plugin entrypoint."""

from git import Repo
from mkdocs.commands import build
from mkdocs.config.base import Config


def test_plugin_builds_newsletters(full_repo: Repo, config: Config) -> None:
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
    """
    __import__("pdb").set_trace()  # XXX BREAKPOINT
    build.build(config)
