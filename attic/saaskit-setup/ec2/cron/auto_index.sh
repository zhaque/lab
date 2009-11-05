#!/bin/bash
wget -O /ebs/web/scripts/dih-out.html "http://127.0.0.1:8983/solr/dataimport?command=full-import&clean=false&optimize=false"
