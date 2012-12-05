#
# docs/Makefile
#
# Development by Carl J. Nobile
#
# This Makefile generates the Resty Code API documtation.
#

FQDN		= $(shell hostname --fqdn)
DOC_DIR		= $(shell pwd)
API_DIR		= rcapi
URL		= http://${FQDN}${DOC_DIR}/${API_DIR}/index.html
TARBALL_NAME	= RestyCodesDocs

all	: api-docs
#----------------------------------------------------------------------
api-docs:
	@(cd ..; epydoc -v --name "Resty Codes" \
          -o docs/${API_DIR} --show-private --show-imports --graph all \
          --url "${URL}" */*.py \
         )
#----------------------------------------------------------------------
tar	:
	@(ln -s ${API_DIR} ${TARBALL_NAME}; \
          tar -chzvf ${TARBALL_NAME}.tar.gz ${TARBALL_NAME})
#----------------------------------------------------------------------
clean	:
	@rm -f *~ \#* .\#*

clobber	: clean
	@rm -rf ${API_DIR} ${TARBALL_NAME} ${TARBALL_NAME}.tar.gz 
