"""Utility functions."""

MESSAGE = """\
Deprecation notice
==================

To avoid name collision with the igraph project, the original igraph visualization
library has been renamed to 'jgraph' in December 2015. The 'igraph' package on
PyPI will soon be used by the igraph project.

The authors of 'jgraph' (ex-igraph) and 'python-igraph' (soon-to-be igraph)
project have agreed on a transition period during which old projects still
using 'igraph' as a PyPI dependency will receive an error while trying to
import igraph in their own projects. The transition period ends on Sep 1 2021.

Things to do now
----------------

If you wanted to install the graph visualization library by Patrick Fuller,
please install 'jgraph' instead. You have time until Sep 1 2021 to do this.

If you wanted to install the Python interface of the igraph network analysis
library, please install 'python-igraph' instead. After Sep 1 2021, you can
start installing 'igraph' instead. 'python-igraph' will keep on working at
least until Sep 1 2022.
"""

def warn_deprecation():
    """Raises a runtime error to warn the user about the upcoming rename of
    python-igraph to igraph.

    Note that we are raising a genuine error here and not a deprecation warning
    as the latter is suppressed by default from Python 2.7 and Python 3.2.
    """
    print(MESSAGE)
    raise RuntimeError("This package is deprecated. See the deprecation notice above.")

