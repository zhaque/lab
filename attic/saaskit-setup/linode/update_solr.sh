#!/bin/bash
cd /ebs/search/solr
svn up
ant clean
ant example
