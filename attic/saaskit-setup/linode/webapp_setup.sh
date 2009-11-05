cd /webapp
git clone git@github.com:CrowdSense/saaskit.git  
chown -R webapp:www-data /webapp/saaskit
git clone git@github.com:CrowdSense/assets.git 
chown -R webapp:www-data /webapp/assets
chmod -R 2750 /webapp/django
