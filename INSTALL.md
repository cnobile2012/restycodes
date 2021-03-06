Resty Codes Installation
========================

Top Level Makefile
------------------

### all

> The `all` target or just make without this target executes the `doc` and
`tar`  targets.

### doc

> The `doc` target generates the EpyDoc API documentation and the PDF file
from the dia diagram.

### tar

> The `tar` target creates a tar file of the entire project including the
generated documentation outside of the project directory. The git meta data
is not included in the tarball.

### tests

> The `tests` target runs the RulesEngine and RestyCodes unit tests.

### python-api

> Creates the python package.

### egg

> Creates the egg file after running the `python-api` target.

### clean

> The `clean` target removes all backup files and python compiled objects.

### clobber

> The `clobber` target removes eveything except the Git source files.


Document Makefile
-----------------

### all

> The `all` target runs the `api-docs` and `pdf` targets. This target is 
usually run from the top level Makefile.

### api-docs

> The `api-docs` target generates the EpyDoc API documentation.

### pdf

> The `pdf` target generates a PDF file from the dia diagram.

### tar

> The `tar` target creates a tar file of the EpyDoc API documentation.

### clean

> The `clean` target removes backup files from the dirs directory.

### clobber

> The `clobber` target runs `clean` target then removes the tar file created 
by the `tar` target.


Installing on the system
------------------------

The installation of the egg file is not included in the Makefile, but can
easily be done with either `easy_install` or `pip`. If you want to install
the code directly running `python setup.py install` will also work.
