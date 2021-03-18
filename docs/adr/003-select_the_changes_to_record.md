Date: 2021-02-12

# Status
<!-- What is the status? Draft, Proposed, Accepted, Rejected, Deprecated or Superseded?
-->
Accepted.

Based on: [002](002-initial_plugin_design.md),
[004](004-article_newsletter_structure.md)

# Context
<!-- What is the issue that we're seeing that is motivating this decision or change? -->
We need to create some logic that reads from the git log to:

* [Extract the last published changes](#extract-the-last-published-changes).  To
    update the articles and feeds, we need to know which changes have been
    already published, so subsequent mkdocs build processes don't repeat work
    already done.

* [Parse the commit messages](#parse-the-commit-messages) to extract the
    semantic versioning information from them.

    The message must follow the [angular commit
    guidelines](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commits)
    with the exception that we'll allow many changes in the same commit message.

* [Extract file context from the MkDocs nav](#extract-the-file-context-from-the-mkdocs-nav)
* [Get the changes that need to be added to the newsletter
    articles](#get-the-commits-that-need-to-be-added-to-the-newsletter-articles).
    We've defined different levels of aggregation for the user to choose how
    often they want to be notified: daily, weekly, monthly or yearly.

# Proposals
<!-- What are the possible solutions to the problem described in the context -->

## Extract the last published changes

We can:

* *Add meaningful tags to the repository*: If we create a tag `last_weekly` on the
    commit of the last published changed for the weekly feed, then we can
    add to the changes to publish only those posterior to that commit.
* *Save the last commit ids in a file in the repo*: If we create a hidden
    `.last_published.json` with the last commit id of each feed type,
    we can add to the feeds only the changes that are posterior to those
    commits.
* *Save the last commit ids in the mkdocs.yaml file*: We can save the last
    commit ids in the configuration section of the plugin in the mkdocs.yaml
    file.
* *Deduce the last published date from existent articles*: We already have this
    information in the existent articles. All we would need to do is analyze the
    files in the `on_files` and deduce the last content publication.

### Add meaningful tags to the repository

Using tags has the advantage that we could reuse the `Repo` object to extract
the information, which we already use in the services that process the changes.
The disadvantage is that we'll pollute the git repository with tags that may not
be interesting to the user. In the digital garden case, it's not a problem, but
it can be in the changelog one.

### Save the last commit ids in a file in the repo

Storing the commit ids in a hidden json file has the advantage that we don't
pollute the git repository, we can use the
[`json`](https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeljson)
export and import functionality of pydantic. The disadvantage is that we'll
create an additional file in the repository.
[cruft](https://cruft.github.io/cruft/) uses this method.

### Save the last commit ids in the mkdocs.yaml file

Storing the commit ids in the mkdocs.yaml file has the advantage that it doesn't
pollute either the git repository nor the project directory. The disadvantage is
that it pollutes the mkdocs configuration file.

### Deduce the last published date from existent articles

Using the existent articles has these advantages:

* It doesn't pollute either the git repository, nor the project directory nor
    the mkdocs configuration file.
* We can fetch the last published date per feed before parsing the commits, so
    instead of analyzing the whole history, we can go from the newest till the
    desired dates, making the algorithm more efficient..
* We don't overwrite the existent articles, so if the user makes changes on
    them, they are respected.

The disadvantage is that we need to code the extraction of that dates from the
files collection, but it should not be difficult.

Assuming that we have the existent articles organized following
[004](004-article_newsletter_structure.md#how-to-organize-the-articles-in-the-mkdocs-nav-and-in-the-repository),
we can create a function that reads the `files` attribute from the `on_files`
event and deduces the date of the last change of the last newsletter article for
each feed.

## Parse the commit messages

We can:

* Use the
    [python-semantic-release](https://python-semantic-release.readthedocs.io/)
    library.
* Use the [commitizen](https://github.com/commitizen-tools/commitizen) library.
* Write our own parser.

After reviewing the existent libraries, I've found that python-semantic-release
exposes the parsed data in a friendlier way. The only drawback is that it uses
NamedTuples for the objects that hold the parsed data, so if we want to change
one, we need to create a new one from the old.

Using an existent library, if it's well maintained, is always better than
writing your own.

## Extract file context from the MkDocs nav

For each file that contains changes, we need to deduce the relative position in
the nav against the rest of articles. This is necessary so we're able to group
changes together by category, subcategory and file later in the [newsletter
creation](005-create_the_newsletter_articles.md).

We can use the
[Deepdiff](https://lyz-code.github.io/blue-book/coding/python/deepdiff/) to
locate the file in the nav tree, and then extract the context information from
the path.

## Get the changes that need to be added to the newsletter articles

For a change to be added to each feed it needs to:

* year: Be made before the first day of the year and after the last published
    change in the year feed.
* month: Be made before the first day of the month and after the last published
    change in the month feed.
* week: Be made before the last Monday and after the last published change in
    the week feed.
* day: Be made before today and after the last published change in the day
    feed.

# Decision
<!-- What is the change that we're proposing and/or doing? -->
We will:

* Run this phase in the
    [`on_files`](https://www.mkdocs.org/user-guide/plugins/#on_files) MkDocs
    event to be able to have the list of articles to process.
* [Deduce the last published date from existent
    articles](#deduce-the-last-published-date-from-existent-articles) as it's
    the cleanest solution in terms of repository pollution.
* Extract the last published dates *before* we parse the commit messages.
* Process only the commits that are posterior to those dates.
* Use python-semantic-release library to parse the commit messages.
* Extract file context from the MkDocs nav
* Get the changes that need to be added to the newsletter articles with the
    different feeds.

# Consequences
<!-- What becomes easier or more difficult to do because of this change? -->
We don't have to write the parsing logic, it's maintained by the community and
it needs few changes to fulfill our needs.

Advantages:

* We'll know between builds which changes have been already published.
* We'll reduce the amount of commits that we parse, thus making the process more
    efficient.
* We wont overwrite manual user changes in the published articles.

Disadvantages:

* We need to code and maintain the extraction of last published date from the
    list of repository files.
