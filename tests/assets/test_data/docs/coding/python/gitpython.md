---
title: GitPython
date: 20210210
author: Lyz
---

[GitPython](https://gitpython.readthedocs.io) is a python library used to
interact with git repositories, high-level like git-porcelain, or low-level like
git-plumbing.

It provides abstractions of git objects for easy access of repository data, and
additionally allows you to access the git repository more directly using either
a pure python implementation, or the faster, but more resource intensive git
command implementation.

The object database implementation is optimized for handling large quantities of
objects and large datasets, which is achieved by using low-level structures and
data streaming.

# [Installation](https://gitpython.readthedocs.io/en/stable/intro.html#installing-gitpython)

```bash
pip install GitPython
```

# Usage

# Testing

There is no testing functionality, you need to either Mock or build fake
adapters.

# References

* [Docs](https://gitpython.readthedocs.io)
* [Git](https://github.com/gitpython-developers/GitPython)
* [Tutorial](https://gitpython.readthedocs.io/en/stable/tutorial.html#tutorial-label)
