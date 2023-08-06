mmf-setup
=========

[![Documentation Status][rtd_badge]][rtd]
[![Tests][ci_badge]][ci]
[![codecov.io][codecov_badge]][codecov]
[![Language grade: Python][lgtm_mmf-setup_badge]][lgtm_mmf-setup]
[![Language grade: Python][lgtm_mmf-setup-fork_badge]][lgtm_mmf-setup-fork]
[![Pypi][PyPI_badge]][PyPI]
[![Python versions][PyPI_versions]][PyPI]
[![Code style: black][black_img]][black]
[![Binder:notebook](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/forbes-group/mmf-setup/branch/default)

This meta-project provides an easy way to install all of the python tools I typically
use. It also serves as a fairly minimal example of setting up a package tate [`pip`] can
install, and specifying dependencies.

In particular, I structure it for the following use-cases:

1. Rapid installation and configuration of the tools I need. For example, I often use
   [CoCalc](cocalc.com). Whenever I create a new project, I need to perform some
   initialization. With this project, it is simply a matter of using [`pip`] to install
   this package, and then using some of the tools. Specifically:

    ```bash
    python3 -m pip install --user mmf-setup
    mmf_setup cocalc

    # OR install from a particular version of the sources.
    python3 -m pip install --user hg+https://alum.mit.edu/www/mforbes/hg/forbes-group/mmf-setup@0.4.0
    mmf_setup cocalc
    ```

2.  Initial setup of a python distribution on a new computer. This is a little more
    involved since one needs to first install python (I recommend using
    [Miniconda](http://conda.pydata.org/miniconda.html)) and then updating the tools.
3.  A place to document various aspects of installing and setting up python and related
    tools. Some of this is old, but kept here for reference.
4.  A generic way of setting sys.path for development work using the following (in order
    of decreasing precedence) by calling `mmf_setup.set_path()`.
    - An entry in a `pyproject.toml` file somewhere in a higher-level directory.
    - An entry in a `setup.cfg` file somewhere in a higher-level directory.
    - The first parent directory with either of these files, a `setup.py` file, or `.hg`
      or `.git` directories.

Quickstart (TL;DR)
==================

1.  To get the notebook initialization features without having to install the package,
    just copy [nbinit.py](nbinit.py) to your project. Importing this will try to execute
    `import mmf_setup;mmf_setup.nbinit()` but failing this, will manually run a similar
    code.
2.  Install this package from the source directory,
    [PyPI](https://pypi.python.org/pypi), etc. with one of the following:

    - **Directly from PyPI**

        ```bash
        python3 -m pip install --user mmf-setup[nbextensions]
        ```
    - **From Source**
        ```bash
        python3 -m pip install --user
        hg+https://alum.mit.edu/www/mforbes/hg/forbes-group/mmf-setup[nbextensions]
        ```

    - **From Local Source** *(Run this from the source directory after you unpack it.)*

        ```bash
        python3 -m pip install --user .[nbextensions]
        ```

    Note: these includes the `nbextensions` extra. You and run without the `--user` flag
    if you want to install them system-wide rather than into [`site.USER_BASE`].

3.  To get the notebook tools for Jupyter (IPython) notebooks, execute the following as
    a code cell in your notebook and then trust the notebook with `File/Trust Notebook`:

    ```python
    import mmf_setup; mmf_setup.nbinit()
    ```

    This will set the theme which is implemented in the output cell so it is stored for
    use online such as when rendered through
    [NBViewer](http://nbviewer.ipython.org). One can specify different
    themes. (Presently only `theme='default'` and `theme='mmf'` are supported.)

4.  **Mercurial:** If you want to install mercurial with the [hg-git] and [Evolve]
    extensions, then you can do that with the `hg` extra:

    ```bash
    python3 -m pip install --user .[hg]
    ```

    This essentially runs `pip install mercurial hg-git hg-evolve`.  You can then enable
    these in your environment by sourcing the `mmf_setup` script in one of the following
    ways:

    ```bash
    eval $"(mmf_setup -v)"     # Enable hg lg but not evolve, etc.
    eval $"(mmf_setup -v -H)"  # Enable evolve, etc.
    mmf_setup -v [-H]          # Shows what will be set set (dry run).
    ```

    To do this automatically when you login, add this line to your `~/.bashc` or
    `~/.bash_profile` scripts.
    
    > **Warning:** the `eval $"(mmf_setup -v -H)"` option also includes a mercurial
    > update hook which will add `%include ../.hgrc` to your projects `.hg/hgrc` file
    > upon `hg > update`.  This allows you to include project-specific mercurial
    > customizations in your repository, but is a potential security risk.  See the
    > discussion below.

    These can also be enabled manually by adding the following to your `~/.hgrc` file:

    ```ini
    # ~/.hgrc
    ...
    [extensions]
    evolve =
    topics =
    hggit =
    ```

Setting `sys.path`
==================

The preferred way to work with python code is to install it, preferably into a virtual
environment or a conda environment. By installing it, you will assure that your program
or library is available to notebooks, etc.  by being properly inserted into
sys.path. When developing, code, one can also do a ["editable"
installs](https://pip.pypa.io/en/stable/reference/pip_install/#local-project-installs)
with `python -m install -e \<path\>` so that code updates are seen.

When developing code, however, this may not meet all use-cases, so we provide
`mmf_utils.set_path(cwd='.')` which will set `mmf_setup.ROOT` and insert it at the start
of `sys.path`. 

The algorithm for determining `ROOT` is as follows starting from `cwd` (which is `'.'`
by default, but can be specified in the call to `set_path()`).  Note: in each case, the
specified path must be an existing directory or it will be ignored.

* A value specified as `mmf_setup.ROOT` will override everything.
* A value in the environmental variable `MMF_SETUP_ROOT` will override everything else.
* An explicit `ROOT` entry in the first `pyproject.toml` found:
    
    ```toml
    # pyproject.toml
    [tool.mmf_setup]
    ROOT = 'src'
    ```
* An explict entry in the first `setup.cfg`:
    
    ```ini
    # setup.cfg
    [mmf_setup]
    ROOT = src
    ```
* The first parent directory to contain any of the files `setup.py`, `setup.cfg`, or
  `pyproject.toml`, or directories `.git`, or `.hg`.

If none of these yields a valid existing directory for `ROOT`, then it will not be set.

Mercurial (hg) Tools
====================

If you source the output of the `mmf_setup` script with one of the following:

```bash
eval $"(mmf_setup -v)"
eval $"(mmf_setup -v -H)"
```

then your `HGRCPATH` will be amended to include
[`hgrc.lga`](src/mmf_setup/_data/hgrc.lga) or
[`hgrc.full`](src/mmf_setup/_data/hgrc.full) respectively.  The first adds a useful `hg
lga` (`hg lg` for short) command which provides a concise graphical display:

```bash
$ hg lg
@  200:d michael (64 minutes ago) 0.4.0[0.4.0] tip
|   ENH,DOC,TST,API: Cleaned up set_path...
o  199:d michael (31 hours ago) 0.4.0[0.4.0]
|   WIP,CHK: Cleaning up set_path.
o  198:d michael (20 hours ago) 0.4.0[0.4.0]
|   DOC: Added developer Notes.md
...
```

The second version with `-H` adds some useful extensions: [hg-git], [Evolve], and
enables [Topics].  The latter are required, for example, to interface with
[Heptapod](https://octobus.net/blog/2019-09-04-heptapod-workflow.html).

Finally, the `-H` option enables an `hg update` hook, which adds `%include ../.hgrc` to
your project's `.hg/hgrc` file when you call `hg update`.  This is a potential security
risk, because an untrusted repo could include dangerous commands in `.hgrc`.  Thus, we
require user intervention before including this:

```bash
$ eval $"(mmf_setup -v -H)"
$ hg clone https://alum.mit.edu/www/mforbes/hg/forbes-group/mmf-setup
...
updating to branch default
88 files updated, 0 files merged, 0 files removed, 0 files unresolved
$ cd mmf-setup
$ hg up 0.4.0
Repository .../mmf-setup contains an .hgrc file.
Including this in .hg/hgrc is a potential security risk.
Only do this if you trust the repository.

Include this .hgrc in .hg/hgrc? [yN]y
Adding '%include ../.hgrc' to '.hg/hgrc'
...
$ tail .hg/hgrc
...
%include ../.hgrc
```


## Notes

See [Notes.md](Notes.md) for developer notes.  Other notes about python, IPython,
etc. are stored in the [docs](docs) folder. 


<!-- Badges -->
[rtd_badge]: <https://readthedocs.org/projects/mmf-setup/badge/?version=latest>
[rtd]: <https://mmf-setup.readthedocs.io/en/latest/?badge=latest>


[drone_badge]: <https://cloud.drone.io/api/badges/forbes-group/mmf-setup/status.svg>
[drone]: https://cloud.drone.io/forbes-group/mmf-setup
[ci_badge]: <https://github.com/mforbes/mmf-setup-fork/actions/workflows/tests.yml/badge.svg>
[ci]: <https://github.com/mforbes/mmf-setup-fork/actions/workflows/tests.yml>

[black]: https://github.com/psf/black
[black_img]: https://img.shields.io/badge/code%20style-black-000000.svg


[lgtm_mmf-setup-fork]: <https://lgtm.com/projects/g/mforbes/mmf-setup-fork/context:python>
[lgtm_mmf-setup-fork_badge]: <https://img.shields.io/lgtm/grade/python/g/mforbes/mmf-setup-fork.svg?logo=lgtm&logoWidth=18>

[lgtm_mmf-setup]: <https://lgtm.com/projects/g/forbes-group/mmf-setup/context:python>
[lgtm_mmf-setup_badge]: <https://img.shields.io/lgtm/grade/python/g/mforbes/mmf-setup.svg?logo=lgtm&logoWidth=18> 

[codecov]: <https://codecov.io/github/mforbes/mmf-setup-fork/branch/default>
[codecov_badge]: <https://codecov.io/github/mforbes/mmf-setup-fork/coverage.svg?branch=default>

[PyPI_badge]: <https://img.shields.io/pypi/v/mmf-setup.svg>
[PyPI_versions]: <https://img.shields.io/pypi/pyversions/mmf-setup.svg>
[PyPI]: <https://pypi.python.org/pypi/mmf-setup> "mmf-setup on PyPI"

<!-- [![Conda -->
<!-- Version](https://img.shields.io/conda/vn/conda-forge/jupytext.svg)](https://anaconda.org/conda-forge/jupytext) -->



<!-- Links -->
[Nox]: <https://nox.thea.codes> "Nox: Flexible test automation"
[Hypermodern Python]: <https://cjolowicz.github.io/posts/hypermodern-python-01-setup/> "Hypermodern Python"
[`pyenv`]: <https://github.com/pyenv/pyenv> "Simple Python Version Management: pyenv"
[`minconda`]: <https://docs.conda.io/en/latest/miniconda.html> "Miniconda"
[Conda]: <https://docs.conda.io> "Conda"
[Heptapod]: <https://heptapod.net> "Heptapod website"
[pytest]: <https://docs.pytest.org> "pytest"
[`pip`]: <https://pip.pypa.io> "pip: the package installer for Python"
[`site.USER_BASE`]: <https://docs.python.org/3/library/site.html#site.USER_BASE>
[Evolve]: <https://www.mercurial-scm.org/doc/evolution/> "Mercurial Evolve extension"
[Topics]: <https://www.mercurial-scm.org/doc/evolution/tutorials/topic-tutorial.html> "Mercurial Topics tutorial"
[hg-git]: <https://hg-git.github.io>
