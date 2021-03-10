Date: 2021-02-12

# Status
<!-- What is the status? Draft, Proposed, Accepted, Rejected, Deprecated or Superseded?
-->
Proposed

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

Even though it seems more easy to create the proposed nav structure in the
`on_files` event, by editing the `nav` dictionary of the `config` object, there
is no way of returning the `config` object in that event, so we're forced to use
the [`on_nav`](https://www.mkdocs.org/user-guide/plugins/#on_nav)
event. The downside of this event is that instead of editing a dictionary, we
need to create the Section, Pages, SectionPages or Link objects and append them
to the `nav.items`, which is more complicated.

We need to define:

* How to translate from a list of newsletter file names to the nav structure.
* Whether to build the nav from scratch on each build or reuse the done job.

## How to translate from a list of newsletter file names to the nav structure

The complex part here is how to get the ordering of the elements in the nav
right. We could:

* Create a `nav_data` dictionary with the following structure:
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
does the new entries fit in so that the nav is still ordered. It makes more
sense to store the `nav_data` object, but building that object is relatively
cheap, so it may not be worth storing it.

# Decision
<!-- What is the change that we're proposing and/or doing? -->
Follow the only proposal regarding the structure, and we'll build the nav
incrementally and we'll store it in a hidden file in
`docs/newsletter/.newsletter_nav.yaml`.

# Consequences
<!-- What becomes easier or more difficult to do because of this change? -->
