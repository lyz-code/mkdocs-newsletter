Date: 2021-02-09

# Status
<!-- What is the status, such as proposed, accepted, rejected, deprecated, superseded,
etc.? -->
Accepted

Based on: [001](001-initial_approach.md)

Extended by: [003](003-select_the_changes_to_record.md),
[004](004-article_newsletter_structure.md), and
[005](005-create_the_newsletter_articles.md).

# Context
<!-- What is the issue that we're seeing that is motivating this decision or change? -->
Taking [001](001-initial_approach.md) as a starting point, we want to define the
processes that the mkdocs plugin need to have to fulfill the desired requirements.

# Proposals
<!-- What are the possible solutions to the problem described in the context -->
The plugin will consist on the following phases:

* [Select the changes that need to be recorded](003-select_the_changes_to_record.md).
* [Create the newsletter articles from those changes](005-create_the_newsletter_articles.md).
* [Build the MkDocs nav with the newsletter articles](004-article_newsletter_structure.md)
* Decide which changes need to be notified
* Send the notifications:
    * Update the RSS
    * Send the email.

# Decision
<!-- What is the change that we're proposing and/or doing? -->
Implement the only proposal.

# Consequences
<!-- What becomes easier or more difficult to do because of this change? -->
