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
        * The next and previos page sections are created.
    """
    build.build(config)  # act

    newsletter_path = f"{full_repo.working_dir}/site/newsletter/2021_02/index.html"
    with open(newsletter_path, "r") as newsletter_file:
        newsletter = newsletter_file.read()
    assert "<title>February of 2021 - The Blue Book</title>" in newsletter
    assert (
        '<nav class="md-nav" aria-label="February of 2021" data-md-level="3">'
        in newsletter
    )
    assert (
        '<a href="../2021_03_02/" class="md-footer__link '
        'md-footer__link--prev" rel="prev">' in newsletter
    )
    assert (
        '<a href="../2021_w06/" class="md-footer__link '
        'md-footer__link--next" rel="next">' in newsletter
    )
