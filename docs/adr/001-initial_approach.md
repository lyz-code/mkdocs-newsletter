Date: 2021-02-08

# Status
<!-- What is the status, such as proposed, accepted, rejected, deprecated, superseded,
etc.? -->
Accepted

Extended by: [002](002-initial_plugin_design.md)

# Context
<!-- What is the issue that we're seeing that is motivating this decision or change? -->

Gathering knowledge in my [blue book](https://lyz-code.github.io/blue-book) has
been a pleasant experience in the last year. The only drawback of the system is
that I don't know a user friendly way to inform the readers of content updates
or fixes, such as an RSS feed of/and a periodic newsletter.

That means that when the user stumbles upon the site, they spend a limited
amount of time reading it, and then forgets of it's existence.

If they see themselves back to the site, they don't know what have they've
already seen, which can make them feel lost or loosing their time.

Even if they clone the repository, they need to [go through the
log](https://github.com/nikitavoloboev/knowledge/issues/19) to see the changes,
which is awful.

And that means that all the efforts we put into growing our [digital
gardens](https://lyz-code.github.io/blue-book/digital_garden/) or our software
applications is not appreciated all that it should be.

If we created a way to show them what has changed in a friendly way we will:

* Make their experience more pleasant.
* Make them more prone to visit the site again.

We must be careful though, we don't want to worsen the bombardment of
information we are suffering. We need to notify the user in a respectful way by
sending them only relevant content at the pace they choose to.

For the idea to work, we'd first need that the authors want to use the solution.
So we need to build a system that doesn't increase the mental load or effort to
a point that makes it unappealing. That can be done by:

* Automating all the processes that we can.
* Reducing to the minimum the author entrypoints.
* Making it easy for them to introduce the manual data that we need.
* Reduce the deviation from their current workflow.

# Proposals
<!-- What are the possible solutions to the problem described in the context -->

To solve the issue we need to decide:

* Which updates are relevant.
* How to reduce the number of notifications the user receives.
* Which notification channels we want to support.
* Which programming solution to use.

## How to extract relevant changes

### Manual processing

At the time of building the update, we could manually review all the changes done since
the last update and store that information in a programmatically processable
way.

The downside is that we'll need to spend a relative big amount of time to review
content written in the past. I found myself skipping these batch processing
tasks in the past, as my brain sees them as dreadful, long and heavy.

### Use semantic versioning in git commit messages

To give semantic meaning to the changes introduced in the repository, we can use the [semantic
versioning](https://semver.org/) principles to classify and describe each change
in a way that can be programmatically decide if it's worth publishing.

The idea is to create commits following [a specific
format](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines)
that describes what kind of change you're making. I've [been following this
practice](https://github.com/lyz-code/blue-book/commits/master) for a while with
the following personal commit convention:

```
{type_of_change}({file_changed}): {short_description}
{full_description}
```

Where:

* `type_of_change` is one of:

  * `feat`: Add new content to the repository, it can be a new file or new content on an
    existent file.
  * `fix`: Correct existing content.
  * `style`: Correct grammar, orthography or broken links.
  * `ci`: Change the continuous integration pipelines.
  * `chore`: Update the python dependencies required to build the site.

* `file_changed`: name of the file changed (without the `.md` extension).
* `short_description`: A succinct description of the change. It doesn't need to
    start with a capitalize letter nor end with a dot.
* `full_description`: A summary of the added changes.

For example: [a single feat
commit](https://github.com/lyz-code/blue-book/commit/5eb3f57da4de99e58bf25ab4b5e24fbb007f7319) or
[a multientry commit](https://github.com/lyz-code/blue-book/commit/53f7b1f67bc7aa2c654e8bfe286d8175e099747b)

With this method the responsibility of giving meaning to the changes is shared
in time, which makes the task more appealing and less heavy. Additionally, with
the IDE support, creating the commit messages is easier as you can copy and
paste or autocomplete from the changes themselves.

## How to reduce the number of notifications

There are cases where the user is still spammed even if we select the relevant
changes.

We can copy the solution adopted by the system's monitorization solutions, which
is to group the changes to reduce the notifications.

We should present different levels of aggregation, so they can receive daily,
weekly or monthly notifications.

## Which notification channels we want to support

Different users use different tools to get updates on what's going in the world.
We can expose the updates through:

* An article in the documentation site.
* RSS.
* Email newsletter.
* API.
* Reddit.
* Hackernews.
* GNUsocial.
* Twitter.
* XMPP/Jabber
* Telegram

The article in the documentation makes sense because it can be the landing page
for the rest of channels, which can trigger further page views.

Most of the people around me, whom I want to share my updates use RSS, which is
an awesome protocol that is sadly being replaced by Twitter like webs, and we
don't want that to happen. I feel that only "technical" users use this
technology though.

Everyone has an email, and sending mails through Python is easy, so it can be
the easiest path to reach the global public.

For the more technical ones, extracting the data from an API can help gluing
together other functionalities. It could help if people want to extend the
functionality that we give, for example by creating more specific RSS feeds
based on categories. As we have a static site, it will only support GET methods,
and we will already publish all the information in RSS format, which is
parseable by programs, so adding another enpoint that exposes the same data in
json format doesn't make much sense.

I haven't used Reddit or Hackernews enough to know if it makes sense either this
channel.

I think GNUsocial and Twitter are wrongly being used to replace RSS, so it won't
be a priority.

A similar argument applies instant message solutions like XMPP or Telegram.

## Which programming solution to use

To create the functionality, we'll need to:

* Semantic versioning information given by the user in the commit messages since
    the last change.
* Link the files mentioned in the commit messages to actual working links.

The processing can be done through:

* A [mkdocs plugin](https://www.mkdocs.org/user-guide/plugins/) so it creates it at
  build time. It can be inspired by:

    * [mkdocs-new-features-notifier](https://pypi.org/project/mkdocs-new-features-notifier/#history)
    * [mkdocs_blog](https://github.com/andyoakley/mkdocs-blog)
    * [mkdocs_latest_release_plugin](https://github.com/agarthetiger/mkdocs_latest_release_plugin)

* An existent external command line tool such as
    [python-semantic-release](https://python-semantic-release.readthedocs.io/en/latest/commit-log-parsing.html)
    and [commitizen bump](https://github.com/commitizen-tools/commitizen).

* A complete new external command line tool.

* An hybrid between both solutions, like [mike](https://github.com/jimporter/mike).

### Developing a mkdocs plugin

The advantages are:

* It will be easier for people to use, as it already exists a widely used plugin
    system in MkDocs.
* It will be easier for us too, as the plugin system gives a lot of information
    on the articles, so making working links should be easy.

The disadvantages are that we'll need to:

* Assume that the user is not meant to manually trigger the updates creation.
    They will need to use a periodic automatic process similar to the one that
    generates the website.

# Decision
<!-- What is the change that we're proposing and/or doing? -->

We will develop a [Mkdocs plugin](#developing-a-mkdocs-plugin) that creates
MkDocs articles whose content:

* Contains only relevant updates, deduced by the [commit
    messages](#use-semantic-versioning-in-git-commit-messages) of the
    repository.
* Updates [are grouped to reduce the user
    notifications](#how-to-reduce-the-number-of-notifications).
* Is exposed to the user with different levels of aggregation, such as: real
    time, daily, weekly, monthly or yearly.
* Is exposed to the user through:
    * Articles in the same MkDocs site.
    * RSS feeds.
    * Email newsletters.

# Consequences
<!-- What becomes easier or more difficult to do because of this change? -->
The user will be able to be kept updated of the relevant MkDocs site changes at
the pace they desire.

That will:

* Make their browsing experience more pleasant.
* Make them more prone to visit the site again.

For the authors it will mean that they need to:

* Spend more time and thought writing the commit messages.
* Be tied to the solution we can give them, or contribute the desired changes.
* Debug possible errors produced by the increase of complexity of the system.

For us it will mean that we'll need to:

* Build and maintain the logic and code for:
    * Extracting and grouping the relevant updates.
    * Sending the notifications.
* Keep the system updated.
* React to security vulnerabilities.
* React to issues and pull requests.
