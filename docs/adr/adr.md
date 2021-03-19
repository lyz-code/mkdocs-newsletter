[ADR](https://lyz-code.github.io/blue-book/adr/) are short text documents that
captures an important architectural decision made along with its context and
consequences.

```mermaid
graph TD
    001[001: High level analysis]
    002[002: Initial MkDocs plugin design]
    003[003: Selected changes to record]
    004[004: Article newsletter structure]
    005[005: Article newsletter creation]

    001 -- Extended --> 002
    002 -- Extended --> 003
    002 -- Extended --> 004
    002 -- Extended --> 005
    003 -- Extended --> 004
    004 -- Extended --> 005

    click 001 "https://lyz-code.github.io/mkdocs-newsletter/adr/001-initial_approach" _blank
    click 002 "https://lyz-code.github.io/mkdocs-newsletter/adr/002-initial_plugin_design" _blank
    click 003 "https://lyz-code.github.io/mkdocs-newsletter/adr/003-select_the_changes_to_record" _blank
    click 004 "https://lyz-code.github.io/mkdocs-newsletter/adr/004-article_newsletter_structure" _blank
    click 005 "https://lyz-code.github.io/mkdocs-newsletter/adr/005-create_the_newsletter_articles" _blank

    001:::accepted
    002:::accepted
    003:::accepted
    004:::accepted
    005:::accepted

    classDef draft fill:#CDBFEA;
    classDef proposed fill:#B1CCE8;
    classDef accepted fill:#B1E8BA;
    classDef rejected fill:#E8B1B1;
    classDef deprecated fill:#E8B1B1;
    classDef superseeded fill:#E8E5B1;
```
