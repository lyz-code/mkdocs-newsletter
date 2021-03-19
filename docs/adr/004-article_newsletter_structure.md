Date: 2021-02-12

# Status
<!-- What is the status? Draft, Proposed, Accepted, Rejected, Deprecated or Superseded?
-->
Accepted

# Context
<!-- What is the issue that we're seeing that is motivating this decision or change? -->
We want to define how to organize the articles that contain the updates as
a section of the MkDocs site in a way that:

* It's easy and pleasant for the user to navigate.
* It's easy for us to parse programmatically.

# Proposals
<!-- What are the possible solutions to the problem described in the context -->

The frequency of updates can be weekly or monthly, structured in a mkdocs nav
similar to:

```yaml
Newsletters:
    - newsletter/0_index.md
    - 2020:
        - newsletter/2020.md
        - February of 2020:
            - newsletter/2020_01.md
            - 6th Week of 2020:
                - newsletter/2020_w06.md
                - 11st February 2020: newsletter/2020_01_01.md
            - 5th Week of 2020:
                - newsletter/2020_w05.md
                - 1st February 2020: newsletter/2020_01_01.md
        - January of 2020:
            - newsletter/2020_01.md
            - 1st Week of 2020:
                - newsletter/2020_w01.md
                - 3rd January 2020: newsletter/2020_01_03.md
                - 1st January 2020: newsletter/2020_01_01.md
```

Where:

* `0_index.md`: Is the landing page of the newsletters. It's prepended with `0_`
    so it shows the first item when you do `ls` in the directory. It will be
    created from a template the first time you run it, then you can change the
    file to fit your liking.
* `2020.md`: Is an automatic year summary done at the end of the year.
* `2020_01.md`: Is an automatic month summary for the monthly rss done at the end
    of the month joining the changes of the month weeks.
* `2020_w01.md`: Is an automatic week summary for the weekly rss done at the
    end of the week joining the changes of the week days.
* `2020_01_01.md`: Is an automatic day summary for the daily rss.

My first idea as a MkDocs user, and newborn plugin developer was to add the
navigation items to the `nav` key in the `config` object, as it's more easy to
add items to a dictionary I'm used to work with than to dive into the code and
understand how MkDocs creates the navigation. As I understood from the
docs, the files should be created in the `on_files` event. the problem with this
approach is that the only event that allows you to change the `config` is the
`on_config` event, which is before the `on_files` one, so you can't build the
navigation this way after you've created the files.

Next idea was to add the items in the `on_nav` event, that means creating
yourself the [`Section`](#section), [`Pages`](#page),
[`SectionPages`](#sectionpage) or `Link` objects and append them to the
`nav.items`.  [The problem](https://github.com/mkdocs/mkdocs/issues/2324) is
that MkDocs initializes and processes the `Navigation` object in the
[`get_navigation`](https://github.com/mkdocs/mkdocs/blob/master/mkdocs/structure/nav.py#L99)
function. If you want to add items with a plugin in the `on_nav` event, you need
to manually run all the post processing functions such as building the `pages`
attribute, by running the `_get_by_type`, ` _add_previous_and_next_links` or
` _add_parent_links` yourself. Additionally, when building the site you'll get
the `The following pages exist in the docs directory, but are not included in
the "nav" configuration` error, because that check is done *before* all plugins
change the navigation in the `on_nav` object.

The last approach is to build the files and tweak the navigation in the
`on_config` event. This approach has the next advantages:

* You need less knowledge of how MkDocs works.
* You don't need to create the `File` or `Files` objects.
* You don't need to create the `Page`, `Section`, `SectionPage` objects.
* More robust as you rely on existent MkDocs functionality.

We need to define:

* How to translate from a list of newsletter file names to the nav structure.
* Whether to build the nav from scratch on each build or reuse the done job.

## How to translate from a list of newsletter file names to the nav structure

The complex part here is how to get the ordering of the elements in the nav
right. We could:

Create a `nav_data` dictionary with the following structure:
    ```yaml
    {
        year: {
            'index': year.md,
            month_number: {
                'index': year_month.md,
                week_number: {
                    'index': year_wweek_number.md,
                    day: year_month_day.md
                }
            }
        }
    }
    ```

And then translate the `nav_data` to the actual `nav` contents.

## Build the nav from scratch or reuse previous run's nav

We can either build the whole newsletter nav each time we build the site or we
can store the nav somewhere and only append the new articles. The second option
is more efficient in terms of energy, I don't want to store in the `mkdocs.yml`
file as the newsletter nav can grow fast, making the file dirty. Another
possibility is to save the nav in `docs/newsletter/.newsletter_nav.yaml`.

If we store the newsletter nav dictionary, it would be difficult to deduce where
does the new entries fit in so that the nav is still ordered. It would make more
sense to store the `nav_data` object, but building that object is relatively
cheap, so it may not be worth even storing it.

# Decision
<!-- What is the change that we're proposing and/or doing? -->
Follow the only proposal regarding the structure, and we'll build the nav
from scratch each time we build the site.

# Consequences
<!-- What becomes easier or more difficult to do because of this change? -->
