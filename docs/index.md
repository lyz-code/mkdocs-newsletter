[![Actions Status](https://github.com/lyz-code/mkdocs-newsletter/workflows/Tests/badge.svg)](https://github.com/lyz-code/mkdocs-newsletter/actions)
[![Actions Status](https://github.com/lyz-code/mkdocs-newsletter/workflows/Build/badge.svg)](https://github.com/lyz-code/mkdocs-newsletter/actions)
[![Coverage Status](https://coveralls.io/repos/github/lyz-code/mkdocs-newsletter/badge.svg?branch=master)](https://coveralls.io/github/lyz-code/mkdocs-newsletter?branch=master)

MkDocs plugin to show the changes of documentation repositories in a user
friendly format, at the same time that it's easy for the authors to maintain.

It creates daily, weekly, monthly and yearly newsletter articles with the
changes of each period. Those pages, stored under the `Newsletters` section, are
filled with the changes extracted from the git history and the commit messages.
The changes are grouped by categories, subcategories and then by file using the
order of the site's navigation structure.

It assumes that you're using [semantic versioning](https://semver.org/) or our
[enhanced version](#commit-message-guidelines) to create your commits. Only
those changes that are interesting to the reader will be added to the
newsletter. You can use
[mkdocs-rss-plugin](https://github.com/Guts/mkdocs-rss-plugin) instead if this
workflow doesn't feel good.

![ ](screencast.gif)

Check [the live
version](https://lyz-code.github.io/blue-book/newsletter/2021_02).

# Installing

```bash
pip install mkdocs-newsletter
```

To enable this plugin, you need to declare it in your config file `mkdocs.yml`.

```yaml
plugins:
  - autolinks
  - section-index
  - mkdocs-newsletter
```

We rely on
[mkdocs-autolink-plugin](https://github.com/midnightprioriem/mkdocs-autolinks-plugin)
to create the links between the articles and on
[mkdocs-section-index](https://github.com/oprypin/mkdocs-section-index/) to make
the sections clickable.

# Usage

Every time you build the site, the plugin will inspect the git history and
create the new newsletter articles under the `docs/newsletter` directory and
configure the `Newsletter` section.

The entrypoints for the authors are:

* [Writing the commit messages](#commit-message-guidelines).
* [Manually changing the created newsletter
    articles](#manual-newsletter-changes): to fix errors.

## Commit message guidelines

The plugin assumes that you're using the [Angular semantic versioning
format](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines)
to create the commits. Adapted to a documentation repository such as the [digital
gardens](https://lyz-code.github.io/blue-book/digital_garden/), the structure
would be:

```
{type_of_change}({file_changed}): {short_description}

{full_description}
```

Where:

* `type_of_change` is one of:

    * `feat`: Add new content to the repository, it can be a new file or new content on an
    existent file.
    * `fix`: Correct existing content.
    * `perf`: Improve existing content.
    * `refactor`: Reorder the articles content.
    * `style`: Correct grammar, orthography or broken links.
    * `ci`: Change the continuous integration pipelines.
    * `chore`: Update the dependencies required to build the site.

* `file_changed`: Name of the changed file (without the `.md` extension).
* `short_description`: A succinct description of the change. It doesn't need to
    start with a capitalize letter nor end with a dot.
* `full_description`: A summary of the added changes.

For example:

```
feat(adr): introduce the Architecture Decision Records

[ADR](https://github.com/joelparkerhenderson/architecture_decision_record) are
short text documents that captures an important architectural decision made
along with its context and consequences.
```

Only changes of type `feat`, `fix`, `perf` or `refactor` will be added to the
newsletter. The reader is not interested in the others.

### Multiple changes in the same commit

When growing [digital
gardens](https://lyz-code.github.io/blue-book/digital_garden/), it's normal to
do many small changes on different files. Making a commit for each of them is
cumbersome and can break your writing flow. That's why the plugin is able to
parse different changes from the same commit. For example:

```
feat(pexpect): introduce the pexpect python library

A pure Python module for spawning
child applications; controlling them; and responding to expected patterns in
their output. Pexpect works like Don Libes’ Expect. Pexpect allows your script
to spawn a child application and control it as if a human were typing commands.

style(prompt_toolkit): correct links and indentations

fix(python_snippets): explain how to show the message in custom exceptions

feat(python_snippets): explain how to import a module or object from within a python program
```

### Link specific parts of the articles

You can specify the section of the article where the change has been made by
appending the anchor to the file changed. For example:

```
perf(prometheus_installation#upgrading-notes): Add upgrading notes from 10.x -> 11.1.7
```

The format of the anchor can be Markdown's default or you can use the user
friendly one with caps and spaces `perf(prometheus_installation#Upgrading
notes)`.

### Rich full description content

The `full_description` content will be processed by MkDocs, that means that all
it's features applies, such as autolinking or admonitions.

~~~markdown
perf(prometheus_installation): Add upgrading notes from 10.x -> 11.1.7

!!! warning "Don't upgrade to 12.x if you're still using Helm 2."

    [Helm](helm.md#version-2) is deprecated and you should migrate to v3.
~~~

## Manual newsletter changes

To change the contents of the newsletters directly edit the files under
`docs/newsletters`.

## Exclude the newsletters from the search

If you don't want to see the newsletters in the result of the search, use the
[mkdocs-exclude-search](https://pypi.org/project/mkdocs-exclude-search/) plugin
to exclude all articles under `docs/newsletter`.

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
