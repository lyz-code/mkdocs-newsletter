
### Update the RSS feed

I'll mimic how [mkdocs-rss-plugin](https://github.com/Guts/mkdocs-rss-plugin)
has already solved the problem, changing the content of the RSS with the HTML of
each of the selected newsletter articles.

Creating an RSS entry for each change, as
[mkdocs-rss-plugin](https://github.com/Guts/mkdocs-rss-plugin) for me it's not
the ideal solution because:

* *The user will receive too many updates*: In a normal day, you can edit up to
    10 files, which will create 10 RSS entries. That can annoy the user so it
    will stop reading your feed.
* *The user will receive updates on irrelevant content*: As an entry is created
    for each change, styling and grammar corrections are sent as a new full
    entry.
* *The user receives no context of the change*: The user is shown the same rss
    entry on creation and on update, so if you change a file often, they will
    see no point on the entry and skip it and in the end drop the RSS.

Keep in mind though that the plugin supports two types of feeds, one for new
content and another for updates, which can reduce the number of notifications.

With this information in the git log we could create RSS feed entries whose:

* Title is taken from `short_description`.
* Body is taken from `full_description`.
* The link to the article can be built from `file_changed`.
* Only `feat` and `fix` entries are evaluated (no one wants to receive an rss
notification of a typo fix in an article).
* An entry will be created for each change, so multientry commits will have many entries.
