apt-get update
apt-get -y upgrade
apt-get -y install --force-yes unzip csstidy build-essential sun-java6-jdk ant subversion git-core mercurial bzr gcc curl python-virtualenv python-git python-imaging python-dev python-setuptools python-egenix-mxdatetime libc6-dev python-ncrypt tofrodos postgresql python-psycopg2 nginx apache2 apache2.2-common apache2-mpm-worker apache2-threaded-dev libapache2-mod-wsgi libapache2-mod-rpaf memcached postfix libmemcache-dev
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
python /usr/local/src/cmemcache-0.95/setup.py install 
python /usr/local/src/cmemcache-0.95/test.py 
rm /usr/local/src/cmemcache-0.95.tar.bz2 
echo "/dev/sdj /ebs/web ext2   noatime  0 0" >> /etc/fstab
echo "/dev/sdk /ebs/db ext2   noatime  0 0" >> /etc/fstab
echo "/dev/sdl /ebs/search ext2   noatime  0 0" >> /etc/fstab
mkdir -p /ebs/web
mkdir -p /ebs/db
mkdir -p /ebs/search
mount /ebs/web
mount /ebs/db
mount /ebs/search
mkdir /var/log/crowdsense
mkdir /var/log/crowdsense/www
mkdir /var/log/crowdsense/assets
mkdir /ebs/web/crowdsense
useradd crowdsense 
usermod -d /ebs/web/crowdsense crowdsense
chown -R crowdsense:www-data /ebs/web/crowdsense
chsh crowdsense -s /bin/bash
git config --global user.name "CrowdSense Admin"
git config --global user.email admin@crowdsense.com
cp /root/.bashrc /ebs/web/crowdsense/.bashrc
cp /root/.gitconfig /ebs/web/crowdsense/.gitconfig
cp /root/.profile /ebs/web/crowdsense/.profile
cp -R /root/.ssh /ebs/web/crowdsense/.ssh
chmod 500 /root/.ssh/id_rsa
chmod 500 /ebs/web/crowdsense/.ssh/id_rsa
mkdir /ebs/web/crowdsense/django
mkdir /ebs/web/crowdsense/django/core
svn co http://code.djangoproject.com/svn/django/trunk/ /ebs/web/crowdsense/django/core
ln -s /ebs/web/crowdsense/django/core/django /usr/local/lib/python2.6/dist-packages/django
python /usr/local/src/cmemcache-0.95/setup.py install 
cd /ebs/web
git clone git@github.com:CrowdSense/setup.git
chown -R crowdsense:www-data /ebs/web/crowdsense
usermod -a -G www-data crowdsense
