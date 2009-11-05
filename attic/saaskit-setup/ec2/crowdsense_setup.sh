su crowdsense 
cd /ebs/web/crowdsense
chmod -R 2750 /ebs/web/crowdsense/django
git clone git@github.com:CrowdSense/assets.git 
ln -s /usr/local/lib/python2.6/dist-packages/django/contrib/admin/media /ebs/web/crowdsense/assets/media/admin
chown -R crowdsense:www-data /ebs/web/crowdsense/assets
cd /ebs/web/crowdsense
#git clone 
chown -R crowdsense:www-data /ebs/web/crowdsense/* 
