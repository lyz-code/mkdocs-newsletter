
## Create the newsletter articles from those changes

Based on [mkdocs-plugin-tags](https://github.com/jldiaz/mkdocs-plugin-tags), the
event to create the newsletter files would be
[on_files](https://www.mkdocs.org/user-guide/plugins/#on_files), which expects
the parameters:

* `files`: global files collection.
* `config`: global configuration object.

And the modified `files` object in return.

An advantage of using the `on_files` event, is that we can rely on the
[autolinks](https://github.com/midnightprioriem/mkdocs-autolinks-plugin) plugin
to resolve the links between the files.

Inspiration:

* [mkdocs-tags](https://github.com/jldiaz/mkdocs-plugin-tags)
* [mkdocs_blog](https://github.com/andyoakley/mkdocs-blog)
* [mkdocs-rss-plugin](https://github.com/Guts/mkdocs-rss-plugin)

We will process each of the changes that need to be recorded and will fill up
a jinja2 template that groups them by category and by article, ordering the
changes chronologically.
