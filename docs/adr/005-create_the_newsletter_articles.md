Date: 2021-02-18

# Status
<!-- What is the status? Draft, Proposed, Accepted, Rejected, Deprecated or Superseded?
-->
Accepted

Based on: [004](004-article_newsletter_structure.md)

# Context
<!-- What is the issue that we're seeing that is motivating this decision or change? -->
We need to present the user the changes in the cleanest way:

* Have the minimum number of title levels, maybe a maximum of 3 levels.
* Group the related changes.

# Proposals
<!-- What are the possible solutions to the problem described in the context -->

To present the changes we want to:

* Group the articles by category and subcategory following the nav order.
* Group the changes by article ordered chronologically.

A TOC doesn't make sense for the article stored in the mkdocs repository as it
is already created by MkDocs.

The skeleton of each article will be:

* Categories as title one, respecting the nav order, with a link to the category
    file if it exists.
* Subcategories as title two, respecting the nav order, with a link to the
    subcategory file if it exists.
* File title as title three, respecting the nav order, with a link to the
    subcategory file if it exists.
* Each change of the file will be added as bullet points ordered by date.
    Where the first line will be the first line of the commit and the body will
    be added below.

    If the scope of the change contains the information of the section of the
    file that it's changing, the link should point to that section instead.

    We need to differentiate the different types of changes:

    * feat: New content additions
    * perf: Improvements on existent articles
    * fix: Corrections on existent articles
    * refactor: Reorganization of articles

We'll then create articles for each feed following the structure defined in
[004](004-article_newsletter_structure.md).

Inspiration:

* [mkdocs-tags](https://github.com/jldiaz/mkdocs-plugin-tags)
* [mkdocs_blog](https://github.com/andyoakley/mkdocs-blog)
* [mkdocs-rss-plugin](https://github.com/Guts/mkdocs-rss-plugin)

# Decision
<!-- What is the change that we're proposing and/or doing? -->
Implement the only proposal.

# Consequences
<!-- What becomes easier or more difficult to do because of this change? -->
