#!/bin/sh
set -eu
set -o vi

#third party repository setting
echo "##### third party repository setting #####";
rpm -ivh http://ftp.riken.jp/Linux/fedora/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -ivh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm
rpm -ivh http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm
cd /etc/yum.repos.d/
wget http://people.centos.org/tru/devtools-2/devtools-2.repo
ls | grep -v -e "CentOS\|devtools" | xargs sed -i -e "s/enabled=1/enabled=0/g"
cd $HOME

# Install packages
echo "##### Install packages #####"
yum -y update
yum -y --enablerepo=epel,remi install httpd bash-completion vim man git

# Python install
echo "##### Python install #####";
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel
sudo yum install python-setuptools -y
sudo easy_install pip

### for skype bot ###
echo "##### for skype bot #####"

# install skype
yum -y --enablerepo=epel install qtwebkit.i686 webkitgtk.i686 qtwebkit
yum -y --enablerepo=epel install glibc.i686 alsa-lib.i686 libXv.i686 libXScrnSaver.i686 qt.i686 gtk2-engines.i686 PackageKit-gtk-module.i686 libcanberra.i686 libcanberra-gtk2.i686
yum -y --enablerepo=epel install pulseaudio-libs.i686 alsa-plugins-pulseaudio.i686
cd /tmp
wget http://download.skype.com/linux/skype-4.2.0.11.tar.bz2
cd /opt
tar xjvf /tmp/skype-4.2.0.11.tar.bz2
rm -f /tmp/skype-4.2.0.11.tar.bz2
ln -s skype-4.2.0.11 skype
ln -s /opt/skype /usr/share/skype
ln -s /opt/skype/skype /usr/bin/skype
dbus-uuidgen > /var/lib/dbus/machine-id

# setup skype for cui
pip install Skype4Py
yum -y install Xvfb x11vnc
yum -y install dbus-x11
# install launch-skype script
git clone https://gist.github.com/557242.git launch-skype
sed -i -e "s/DAEMON_USER=skype/DAEMON_USER=root/g" launch-skype/launch-skype.sh
chmod 755 launch-skype/launch-skype.sh
mv launch-skype/launch-skype.sh /etc/init.d/
rm -rf launch-skype
#! must change USERNAME, PASSWORD in /etc/init.d/launch-skype.sh
#! must auth skype process with vnc:
#  /etc/init.d/launch-skype.sh start
#  x11vnc -display :20 -xauth /var/run/skype/Xauthority &
#  ( auth skype and check auto login with vnc )

# setup python program
pip install google-api-python-client httplib2 python-gflags pytz argparse
yum -y install firefox # need oauth google api
# ( cp or clone *.py )
# env DISPLAY=:20 XAUTHORITY=/var/run/skype/Xauthority python skype-bot.py
# ( open firefox and auth google with vnc )

# Disable iptables
echo "##### Disable iptables  #####"
/sbin/chkconfig iptables off
/sbin/service iptables stop

# Disable SELinux
echo "##### Disable SELinux #####"
/usr/sbin/setenforce 0
/bin/sed -i -e "s/SELINUX=permissive/SELINUX=disabled/g" /etc/selinux/config

echo "### all completed! ###"
