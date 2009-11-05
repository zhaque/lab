apt-get update
apt-get -y upgrade
apt-get -y install --force-yes nmap unzip wget csstidy build-essential sun-java6-jdk ant subversion git-core mercurial bzr gcc curl python-virtualenv python-git python-imaging python-dev python-setuptools python-egenix-mxdatetime libc6-dev python-ncrypt tofrodos postgresql python-psycopg2 nginx apache2 apache2.2-common apache2-mpm-worker apache2-threaded-dev libapache2-mod-wsgi libapache2-mod-rpaf memcached postfix libmemcache-dev
apache2ctl stop
a2dissite 000-default
/etc/init.d/nginx stop
rm /etc/apache2/sites-enabled/*
rm /etc/nginx/sites-enabled/*
/etc/init.d/postgresql-8.3 stop 
/usr/bin/easy_install egenix-mx-base
/usr/bin/easy_install psycopg2
cd /usr/local/src/
wget http://gijsbert.org/downloads/cmemcache/cmemcache-0.95.tar.bz2
tar xjvf cmemcache-0.95.tar.bz2
cd /usr/local/src/cmemcache-0.95/ 
python setup.py install 
python test.py 
rm /usr/local/src/cmemcache-0.95.tar.bz2 
echo "/dev/xvdc /webapp ext3   noatime  0 0" >> /etc/fstab
echo "/dev/xvdd /database ext3   noatime  0 0" >> /etc/fstab
mkdir -p /webapp
mkdir -p /database
mount /webapp
mount /database
mkdir /var/log/webapp
mkdir /var/log/webapp/main
mkdir /var/log/webapp/assets
mkdir /var/log/webapp/user_sites
useradd webapp 
usermod -d /webapp webapp 
chown -R webapp:www-data /webapp
chsh webapp -s /bin/bash
mkdir /webapp/django
mkdir /webapp/django/core
svn co http://code.djangoproject.com/svn/django/trunk/ /webapp/django/core
ln -s /webapp/django/core/django /usr/local/lib/python2.6/dist-packages/django
chown -R webapp:www-data /webapp
usermod -a -G www-data webapp 
git config --global user.name "CrowdSense"
git config --global user.email admin@crowdsense.com
cp /root/.bashrc /webapp/.bashrc
cp /root/.gitconfig /webapp/.gitconfig
cp /root/.profile /webapp/.profile
cp -R /root/.ssh /webapp/.ssh
chmod 500 /root/.ssh/id_rsa
chmod 500 /webapp/.ssh/id_rsa
chown -R webapp:www-data /webapp
