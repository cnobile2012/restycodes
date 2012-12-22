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
generated documentation, but without the git meta data outside of the
project directory.

### tests

> The `tests` target runs the RulesEngine and RestyCodes unit tests.

### egg

> TODO -- Will create an egg file for installing the RestyCodes package.

### clean

> The `clean` target removes all backup files and python compiled objects.

### clobber

> The `clobber` target removes eveything except the Git source files.


Document Makefile
-----------------

### all

> The `all` target runs the `api-docs` and `pdf` targets.

### api-docs

> The `api-docs` target is usually run from the top level Makefile. It
generates the EpyDoc API documentation.

### pdf

> The `pdf` target generates a PDF file from the dia diagram.

### tar

> The `tar` target creates a tar file of the EpyDoc API documentation.

### clean

> The `clean` target removes backup files from the dirs directory.

### clobber

> The `clobber` target runs `clean` target then removes the tar file created 
by the `tar` target.
