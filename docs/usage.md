Every time you build the site, the plugin will inspect the git history and
create the new newsletter articles under the `docs/newsletter` directory and
configure the `Newsletter` section.

The entrypoints for the authors are:

* [Writing the commit messages](#commit-message-guidelines).
* [Manually changing the created newsletter
    articles](#manual-newsletter-changes): to fix errors.

# Commit message guidelines

The plugin assumes that you're using the [Angular semantic versioning
format](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines)
to create the commits. Adapted to a documentation repository such as the [digital
gardens](https://lyz-code.github.io/blue-book/digital_garden/), the structure
would be:

```
{type_of_change}({file_changed}): {short_description}

{full_description}
```

Where:

* `type_of_change` is one of:

    * `feat`: Add new content to the repository, it can be a new file or new content on an
    existent file.
    * `fix`: Correct existing content.
    * `perf`: Improve existing content.
    * `refactor`: Reorder the articles content.
    * `style`: Correct grammar, orthography or broken links.
    * `ci`: Change the continuous integration pipelines.
    * `chore`: Update the dependencies required to build the site.

* `file_changed`: Name of the changed file (without the `.md` extension).
* `short_description`: A succinct description of the change. It doesn't need to
    start with a capitalize letter nor end with a dot.
* `full_description`: A summary of the added changes.

For example:

```
feat(adr): introduce the Architecture Decision Records

[ADR](https://github.com/joelparkerhenderson/architecture_decision_record) are
short text documents that captures an important architectural decision made
along with its context and consequences.
```

Only changes of type `feat`, `fix`, `perf` or `refactor` will be added to the
newsletter. The reader is not interested in the others.

## Multiple changes in the same commit

When growing [digital
gardens](https://lyz-code.github.io/blue-book/digital_garden/), it's normal to
do many small changes on different files. Making a commit for each of them is
cumbersome and can break your writing flow. That's why the plugin is able to
parse different changes from the same commit. For example:

```
feat(pexpect): introduce the pexpect python library

A pure Python module for spawning
child applications; controlling them; and responding to expected patterns in
their output. Pexpect works like Don Libes’ Expect. Pexpect allows your script
to spawn a child application and control it as if a human were typing commands.

style(prompt_toolkit): correct links and indentations

fix(python_snippets): explain how to show the message in custom exceptions

feat(python_snippets): explain how to import a module or object from within a python program
```

## Link specific parts of the articles

You can specify the section of the article where the change has been made by
appending the anchor to the file changed. For example:

```
perf(prometheus_installation#upgrading-notes): Add upgrading notes from 10.x -> 11.1.7
```

The format of the anchor can be Markdown's default or you can use the user
friendly one with caps and spaces `perf(prometheus_installation#Upgrading
notes)`.

## Rich full description content

The `full_description` content will be processed by MkDocs, that means that all
it's features applies, such as autolinking or admonitions.

~~~markdown
perf(prometheus_installation): Add upgrading notes from 10.x -> 11.1.7

!!! warning "Don't upgrade to 12.x if you're still using Helm 2."

    [Helm](helm.md#version-2) is deprecated and you should migrate to v3.
~~~

# Manual newsletter changes

To change the contents of the newsletters directly edit the files under
`docs/newsletters`.
