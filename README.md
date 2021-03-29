# MkDocs Newsletter

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

## Help

See [documentation](https://lyz-code.github.io/mkdocs-newsletter) for more details.

## [Installing](https://lyz-code.github.io/mkdocs-newsletter/install/)

You should check the [install
docs](https://lyz-code.github.io/mkdocs-newsletter/install/), but in short,
you'll need to:

```bash
pip install mkdocs-newsletter
```

And enable this plugin, by changing your `mkdocs.yml`.

```yaml
plugins:
  - git-revision-date-localized:
      type: timeago
  - autolinks
  - section-index
  - mkdocs-newsletter
```

## Contributing

For guidance on setting up a development environment, and how to make
a contribution to *mkdocs-newsletter*, see [Contributing to
mkdocs-newsletter](https://lyz-code.github.io/mkdocs-newsletter/contributing).

## License

GPLv3
