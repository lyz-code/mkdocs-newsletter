Date: 2021-03-26

# Status
<!-- What is the status? Draft, Proposed, Accepted, Rejected, Deprecated or Superseded?
-->
Accepted

# Context
<!-- What is the issue that we're seeing that is motivating this decision or change? -->
We want the readers to be notified by RSS of the changes of the documentation
site. They should be able to choose the frequency of the updates.

# Proposals
<!-- What are the possible solutions to the problem described in the context -->

Once the newsletter mkdocs articles are created, we need to expose them through
RSS feeds for each of the periodicities (daily, weekly, monthly and yearly).

We have the newsletter articles both in markdown and in html if we use the
[`on_post_build`](https://www.mkdocs.org/user-guide/plugins/#on_post_build)
event.

We need to create both the RSS site documentation and the entries content. The
first one can be created with the contents of the mkdocs `config` object, the
second ones using the html might be more interesting as it will have already the
internal links resolved to working urls.

We'll refactor the code from
[mkdocs-rss-plugin](https://github.com/Guts/mkdocs-rss-plugin), as they've
already solved the problem of creating an RSS for a MkDocs site.

We need to decide:

* [How to select the newsletters to be published in each
    feed.](#newsletter-selection)
* [How to create each feed.](#how-to-create-each-feed)

## Newsletter selection

We're going to expose 15 entries in each feed.

To get the 15 last newsletters for each feed we need to analyze the existent
elements in the newsletter directory and then see the latest modification date
of each of them.

The `published_date` of the channel must be the published date of the last entry
of the feed.

## How to create each feed

We'll use the mkdocs-rss-plugin jinja2 template. I tried to use feedparser, but
it's only for parsing and not for building RSSs.

# Decision
<!-- What is the change that we're proposing and/or doing? -->
Implement the only proposal.

# Consequences
<!-- What becomes easier or more difficult to do because of this change? -->
