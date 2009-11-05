cp /ebs/web/setup/boot/nginx/assets /etc/nginx/sites-available/assets
ln -s /etc/nginx/sites-available/assets /etc/nginx/sites-enabled/assets
cp /ebs/web/setup/boot/nginx/www /etc/nginx/sites-available/www
ln -s /etc/nginx/sites-available/www /etc/nginx/sites-enabled/www
cp /ebs/web/setup/boot/apache/www  /etc/apache2/sites-available/www 
a2ensite www
cp /ebs/web/setup/boot/nginx/nginx.conf /etc/nginx/nginx.conf
cp /ebs/web/setup/boot/nginx/proxy.conf /etc/nginx/proxy.conf
cp /ebs/web/setup/boot/apache/apache2.conf /etc/apache2/apache2.conf
cp /ebs/web/setup/boot/apache/ports.conf /etc/apache2/ports.conf
cp /ebs/web/setup/boot/apache/security /etc/apache2/conf.d/security
cp /ebs/web/setup/boot/db/initial_db.tar /ebs/db
cd /ebs/db
tar xvf initial_db.tar 
chown -R postgres:postgres /ebs/db/postgresql
rm -rf /ebs/db/initial_db.tar
cp /ebs/web/setup/boot/db/postgresql.conf /etc/postgresql/8.3/main/postgresql.conf
cp /ebs/web/setup/boot/db/pg_hba.conf /etc/postgresql/8.3/main/pg_hba.conf 
chown -R crowdsense:www-data /ebs/web/crowdsense
apt-get -y autoremove
/etc/init.d/postgresql-8.3 start
/etc/init.d/nginx start
/etc/init.d/apache2 start
