
## Update the RSS and send the email.

When we want to generate the RSS feed or the newsletter, we can do it in the
[`on_post_build`](https://www.mkdocs.org/user-guide/plugins/#on_post_build)
event, as [mkdocs-rss-plugin](https://github.com/Guts/mkdocs-rss-plugin) does,
maybe we can directly take the html of the newly generated newsletters and
inject it in an email and in each RSS entry. This approach has another
advantage, if the user changes the generated markdown newsletters, then the
changes are automatically migrated to the RSS entries, not to the emails if they
are already sent though.
