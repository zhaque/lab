#!/bin/sh
SOLR_HOME=`pwd`
cd ../upstream/apache-solr/example
exec java \
    -Dsolr.solr.home="$SOLR_HOME" \
    -Dsolr.data.dir="$SOLR_HOME/data/" \
    -jar start.jar
