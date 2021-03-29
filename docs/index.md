[![Actions Status](https://github.com/lyz-code/mkdocs-newsletter/workflows/Tests/badge.svg)](https://github.com/lyz-code/mkdocs-newsletter/actions)
[![Actions Status](https://github.com/lyz-code/mkdocs-newsletter/workflows/Build/badge.svg)](https://github.com/lyz-code/mkdocs-newsletter/actions)
[![Coverage Status](https://coveralls.io/repos/github/lyz-code/mkdocs-newsletter/badge.svg?branch=master)](https://coveralls.io/github/lyz-code/mkdocs-newsletter?branch=master)

MkDocs plugin to show the changes of documentation repositories in a user
friendly format, at the same time that it's easy for the authors to maintain.

It creates daily, weekly, monthly and yearly newsletter articles with the
changes of each period. Those pages, stored under the `Newsletters` section, are
filled with the changes extracted from the git history and the commit messages.
The changes are grouped by categories, subcategories and then by file using the
order of the site's navigation structure. [RSS feeds](rss_feeds.md) are also
created for each newsletter type, so it's easy for people to keep updated with
the evolution of the site.

It assumes that you're using [semantic versioning](https://semver.org/) or our
[enhanced version](#commit-message-guidelines) to create your commits. Only
those changes that are interesting to the reader will be added to the
newsletter. You can use
[mkdocs-rss-plugin](https://github.com/Guts/mkdocs-rss-plugin) instead if this
workflow doesn't feel good.

![ ](screencast.gif)

Check [a live
version](https://lyz-code.github.io/blue-book/newsletter/0_newsletter_index/).

# Alternatives

## [mkdocs-rss-plugin](https://github.com/Guts/mkdocs-rss-plugin)

This cool plugin creates two RSS feeds for the changes of the git history, one
for new files and another for updated ones.

Creating an RSS entry for each change, it's not the ideal solution for digital
gardens because:

* *The user will receive too many updates*: In a normal day, you can edit up to
    10 files, which will create 10 RSS entries. That can annoy the user so it
    will stop reading your feed.
* *The user will receive updates on irrelevant content*: As an entry is created
    for each change, styling and grammar corrections are sent as a new full
    entry.
* *The user receives no context of the change*: The RSS entry links to the
    article but not it's sections, so if you frequently edit a big file, the,
    the user will see no point on the entry and skip it and in the end drop the
    RSS.

If you feel that your use case wont suffer from those conditions, I suggest you
use their plugin instead, as it's much easier to use.

# Future plans

The plugin will reach the first stable version once we:

* Support more notification channels such as RSS feeds and email newsletters.

We're also thinking of adding support for software repositories, to give updates
on the releases.

# References

As most open sourced programs, `mkdocs-newsletter` is standing on the shoulders of
giants, namely:

[Pytest](https://docs.pytest.org/en/latest)
: Testing framework, enhanced by the awesome
    [pytest-cases](https://smarie.github.io/python-pytest-cases/) library that made
    the parametrization of the tests a lovely experience.

[Mypy](https://mypy.readthedocs.io/en/stable/)
: Python static type checker.

[Flakehell](https://github.com/life4/flakehell)
: Python linter with [lots of
    checks](https://lyz-code.github.io/blue-book/devops/flakehell/#plugins).

[Black](https://black.readthedocs.io/en/stable/)
: Python formatter to keep a nice style without effort.

[Autoimport](https://github.com/lyz-code/autoimport)
: Python formatter to automatically fix wrong import statements.

[isort](https://github.com/timothycrosley/isort)
: Python formatter to order the import statements.

[Pip-tools](https://github.com/jazzband/pip-tools)
: Command line tool to manage the dependencies.

[Mkdocs](https://www.mkdocs.org/)
: To build this documentation site, with the
[Material theme](https://squidfunk.github.io/mkdocs-material).

[Safety](https://github.com/pyupio/safety)
: To check the installed dependencies for known security vulnerabilities.

[Bandit](https://bandit.readthedocs.io/en/latest/)
: To finds common security issues in Python code.

[Yamlfix](https://github.com/lyz-code/yamlfix)
: YAML fixer.

# Contributing

For guidance on setting up a development environment, and how to make
a contribution to *mkdocs-newsletter*, see [Contributing to
mkdocs-newsletter](https://lyz-code.github.io/mkdocs-newsletter/contributing).
