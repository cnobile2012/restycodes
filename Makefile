#
# Makefile for the RESTful Response Codes package.
#
# Development by Carl J. Nobile
#

PREFIX		= $(shell pwd)
PACKAGE_DIR	= $(shell echo $${PWD\#\#*/})
RULES_ENGINE	= rulesengine
RESTY_CODES	= restycodes
DOCS_DIR	= $(PREFIX)/docs

#----------------------------------------------------------------------
all	: doc tar

#----------------------------------------------------------------------
doc	:
	@(cd $(DOCS_DIR); make)
#----------------------------------------------------------------------
tar	: clean
	@(cd ..; tar -czvf $(PACKAGE_DIR).tar.gz --exclude=".git" \
          $(PACKAGE_DIR))
#----------------------------------------------------------------------
clean	:
	@rm -f *~ \#* .\#* *.pyc
	@(cd ${RULES_ENGINE}; rm -f *~ \#* .\#* *.pyc)
	@(cd ${RESTY_CODES}; rm -f *~ \#* .\#* *.pyc)
	@(cd ${DOCS_DIR}; make clean)

clobber	: clean
	@(cd $(DOCS_DIR); make clobber)
