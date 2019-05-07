Developing
==========

The `WhatsHap source code is on Bitbucket <https://bitbucket.org/whatshap/whatshap/>`_.
WhatsHap is developed in Python 3, Cython and C++.


Development installation
------------------------

For development, make sure that you install Cython and tox. We also recommend
using a virtualenv. This sequence of commands should work::

	git clone https://bitbucket.org/whatshap/whatshap
	cd whatshap
	python3 -m venv venv
	source venv/bin/activate
	pip install -e .[dev]

The last command installs also all the development dependencies, such as Cython. Use only
``pip install -e .`` to omit those.

Next, you can run WhatsHap like this::

	whatshap --help


Development installation when using Conda
-----------------------------------------

If you are using `Bioconda <https://bioconda.github.io/>`_, it is convenient to develop WhatsHap in a separate environment::

	conda create -n whatshap-dev python=3.6 pysam PyVCF pyfaidx xopen Cython pytest sphinx-issues
	source activate whatshap-dev
	git clone https://bitbucket.org/whatshap/whatshap
	cd whatshap
	pip install -e .

The last command installs WhatsHap into your Conda environment named ``whatshap-dev``. So when
executing ``whatshap`` you will run the latest version you just cloned.

Running tests
-------------

While in the virtual environment, you can run the tests for the current Python version like this::

	pytest

Whenever you change any Cython code (``.pyx`` files), you need to re-run the
``pip install -e .`` step in order to compile it.

Optionally, to run tests for *all* supported Python versions, you can run
`tox <https://tox.readthedocs.io/>`_. It creates separate virtual environments for each Python
version, installs WhatsHap into it and then runs the tests. It also tests documentation generation
with ``sphinx``. Run it like this::

    tox

If ``tox`` is installed on the system, you do not need to be inside a virtual environment for this.
However, you need to have all tested Python versions installed on the system! See the instructions
below for how to do this on Ubuntu.


Installing other Python versions in Ubuntu
------------------------------------------

Ubuntu comes with one default Python 3 version, and in order to test WhatsHap
with older or newer Python versions, follow the instructions for enabling the
`“deadsnakes” repository <https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa>`_.
After you have done so, ensure you have the following packages::

	sudo apt install build-essential python-software-properties

Then get and install the desired Python versions. Make sure you install the ``-dev`` package.
For example, for Python 3.4::

	sudo apt update
	sudo apt install python3.4-dev


Debugging
---------

Here is one way to get a backtrace from gdb (assuming the bug occurs while
running the tests)::

	$ gdb python3
	(gdb) run -m pytest

After you get a SIGSEGV, let gdb print a backtrace:

	(gdb) bt


Wrapping C++ classes
--------------------

The WhatsHap phasing algorithm is written in C++, as are many of the core
data structures such as the “Read” class. To make the C++ classes usable from
Python, we use Cython to wrap the classes. All these definitions are spread
across multiple files. To add new attributes or methods to an existing class
or to add a new class, changes need to be made in different places.

Let us look at the “Read” class. The following places in the code may need to
be changed if the Read class is changed or extended:

* ``src/read.cpp``: Implementation of the class (C++).
* ``src/read.h``: Header with the class declaration (also normal C++).
* ``whatshap/cpp.pxd``: Cython declarations of the class. This repeats – using
  the Cython syntax this time – a subset of the information from the
  ``src/read.h`` file. This duplication is required because Cython
  cannot read ``.h`` files (it would need a full C++ parser for that).

  Note that the ``cpp.pxd`` file contains definitions for *all* the ``.h``
  headers. (It would be cleaner to have them in separate ``.pxd`` files, but
  this leads to problems when linking the compiled files.)
* ``whatshap/core.pxd``: This contains declarations of all *Cython* classes
  wrapping C++ classes. Note that the class ``Read`` in this file has the
  same name as the C++ class, but that it is not the same as the C++ one!
  The distinction is made by prefixing the C++ class with ``cpp.``, which is
  the name of the module in which it is declared in (that is, the C++ class
  ``Read`` is declared in ``cpp.pxd``). The wrapping (Cython) class ``Read``
  stores the C++ class in an attribute named ``thisptr``. If you add a new
  class, it needs to be added to this file. If you only modify an existing one,
  you probably do not need to change this file.
* ``whatshap/core.pyx``: The Cython implementation of the wrapper classes.
  Again, the name ``Read`` by itself is the Python wrapper class and
  ``cpp.Read`` is the name for the C++ class.

Before adding yet more C++ code, which then requires extra code for wrapping it,
consider writing an implementation in Cython instead. See ``readselect.pyx``,
for example, which started out as a Python module and was then transferred to
Cython to make it faster. Here, the Cython code is not merely a wrapper, but
contains the implementation itself.


Writing documentation
---------------------

Documentation is located in the ``doc/`` subdirectory. It is written in
`reStructuredText format <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
and is translated by `Sphinx <http://www.sphinx-doc.org/>`_ into HTML format.

Documentation is hosted on `Read the Docs <https://readthedocs.org/>`_.
In theory, it is built automatically whenever a commit is made. The documentation in the
``master`` branch should be visible at `https://whatshap.readthedocs.io/en/latest/ <https://whatshap.readthedocs.io/en/latest/>`_
and documentation for the most recent released version should be visible at `https://whatshap.readthedocs.io/en/stable/ <https://whatshap.readthedocs.io/en/stable/>`_.
However, the connection between Bitbucket and Read the Docs has never worked
well in this particular project, so builds actually need to be triggered manually
until we have solved this problem.

To generate documentation locally, ensure that you installed sphinx and add-ons
necessary to build documantation (running ``pip install -e .[dev]`` will take
care of this). Then go into the ``doc/`` directory and run ``make``. You can
then open ``doc/_build/html/index.html`` in your browser. The theme that is
used is a bit different from the one the Read the Docs uses.


Making a release
----------------

If this is the first time you attempt to upload a distribution to PyPI, create a
configuration file named ``.pypirc`` in your home directory with the following
contents::

	[distutils]
	index-servers =
	    pypi

	[pypi]
	username=my-user-name
	password=my-password

See also `this blog post about getting started with
PyPI <http://peterdowns.com/posts/first-time-with-pypi.html>`_. In particular,
note that a ``%`` in your password needs to be doubled and that the password
must *not* be put between quotation marks even if it contains spaces.

#. Set the correct version number in the changelog. Ensure that the list of changes is up-to-date.

#. Ensure you have no uncommitted changes in the working copy.

#. Run ``tox``, ensuring all tests pass.

#. Tag the current commit with the version number (there must be a ``v`` prefix)::

       git tag v0.1

#. Create a distribution (``.tar.gz`` file), ensuring that the auto-generated version number in
   the tarball is as you expect it::

       python3 setup.py sdist

#. Upload the distribution to PyPI (the tarball must be regenerated since ``upload`` requires a preceding ``sdist``)::

       twine upload dist/whatshap-x.yz.tar.gz

   You may need to install the ``twine`` tool to run this command.
#. Push the tag::

       git push --tags

#. Update the `bioconda recipe <https://github.com/bioconda/bioconda-recipes/blob/master/recipes/whatshap/meta.yaml>`_.
   It is probly easiest to edit the recipe via the web interface and send in a
   pull request. Ensure that the list of dependencies (the ``requirements:``
   section in the recipe) is in sync with the ``setup.py`` file.

   Since this is just a version bump, the pull request does not need a
   review by other bioconda developers. As soon as the tests pass and if you
   have the proper permissions, it can be merged directly.

If something went wrong, fix the problem and follow the above instructions again,
but with an incremented revision in the version number. That is, go from version
x.y to x.y.1. Do not change a version that has already been uploaded.


Adding a new subcommand
-----------------------

Follow the instructions in ``whatshap/example.py``.
