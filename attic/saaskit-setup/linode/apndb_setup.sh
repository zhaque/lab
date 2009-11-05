cp /root/setup/linode/boot/nginx/assets /etc/nginx/sites-available/assets
ln -s /etc/nginx/sites-available/assets /etc/nginx/sites-enabled/assets
cp /root/setup/linode/boot/nginx/webapp /etc/nginx/sites-available/webapp
ln -s /etc/nginx/sites-available/webapp /etc/nginx/sites-enabled/webapp
cp /root/setup/linode/boot/apache/main  /etc/apache2/sites-available/main 
cp /root/setup/linode/boot/apache/sites  /etc/apache2/sites-available/sites 
a2ensite main
a2ensite sites 
cp /root/setup/linode/boot/nginx/nginx.conf /etc/nginx/nginx.conf
cp /root/setup/linode/boot/nginx/proxy.conf /etc/nginx/proxy.conf
cp /root/setup/linode/boot/apache/apache2.conf /etc/apache2/apache2.conf
cp /root/setup/linode/boot/apache/ports.conf /etc/apache2/ports.conf
cp /root/setup/linode/boot/apache/security /etc/apache2/conf.d/security
cp /root/setup/linode/boot/db/initial_db.tar /database
cd /database
tar xvf initial_db.tar 
chown -R postgres:postgres /database/postgresql
rm -rf /database/initial_db.tar
cp /root/setup/linode/boot/db/postgresql.conf /etc/postgresql/8.3/main/postgresql.conf
cp /root/setup/linode/boot/db/pg_hba.conf /etc/postgresql/8.3/main/pg_hba.conf 
chown -R webapp:www-data /webapp
apt-get -y autoremove
/etc/init.d/postgresql-8.3 start
/etc/init.d/nginx start
/etc/init.d/apache2 start
