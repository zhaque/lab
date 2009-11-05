cp -R ~/solr\ svn/trunk/example ~/solrserver 

rm -R -f ~/solrserver/solr/conf
ln -s ~/mashup/misc/solr/conf ~/solrserver/solr/conf 

cd ~/solrserver 
java -jar start.jar  
