Date: 2021-02-12

# Status
<!-- What is the status? Draft, Proposed, Accepted, Rejected, Deprecated or Superseded?
-->
Draft

# Context
<!-- What is the issue that we're seeing that is motivating this decision or change? -->
We want to define how to organize the articles that contain the updates as
a section of the MkDocs site in a way that:

* It's easy and pleasant for the user to navigate.
* It's easy for us to parse programmatically.

That means defining:

* The article structure.
* How to organize the articles in the MkDocs nav and in the repository.

# Proposals
<!-- What are the possible solutions to the problem described in the context -->

## Article structure

We want the newsletter to present the changes grouped by article in
a chronological order, the articles can also be grouped by the main nav category
, a TOC doesn't make sense for the article stored in the mkdocs repository, but
it can for the email or RSS entries.

The frequency of updates can be weekly or monthly, structured in a mkdocs nav
similar to:

```yaml
Newsletters:
    - 2021:
        - January:
            - Week 1: 2021_01_1.md
    - 2020:
        - 2020.md
        - January:
            - 2020_01.md
            - Week 1: 2020_01_1.md
            - Week 2: 2020_02_2.md
```

Where:

* `2020.md`: Is an automatic year summary done at the end of the year.
* `2020_01.md`: Is an automatic month summary for the monthly rss done at the end
    of the month joining the changes of the month weeks.
* `2020_01_1.md`: Is an automatic week summary for the weekly rss done at the
    end of the week joining the changes of the week days.

To create the newsletter we need to process the following data:

* Semantic versioning information given by the user in the commit messages since
    the last change.
* Link the files mentioned in the commit messages to actual working links.

# Decision
<!-- What is the change that we're proposing and/or doing? -->

# Consequences
<!-- What becomes easier or more difficult to do because of this change? -->
