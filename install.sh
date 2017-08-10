#!/bin/bash
SCRIPTNAME="blinktemp"
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi
echo "Checking dependency requirements..."
if [ $(dpkg-query -W -f='${Status}' dos2unix 2>/dev/null | grep -c "ok installed") -eq 0 ]; then
    apt-get install -y dos2unix;
else
    echo "---dos2unix already installed"
fi
if [ $(dpkg-query -W -f='${Status}' python2.7-dev 2>/dev/null | grep -c "ok installed") -eq 0 ]; then
    apt-get install -y python-pip python2.7-dev;
	easy_install pip;
	echo "---python installed"
else
    echo "---python2.7-dev already installed"
fi
if [ $(pip list | grep -F "blinkstick") -eq 0 ]; then
    pip install blinkstick;
	echo "---blinkstick python module installed"
else
    echo "---blickstick python module already installed."
fi
if [ $(pip list | grep -F "psutil") -eq 0 ]; then
    pip install psutil;
else
    echo "---psutil python system monitor already installed."
fi
echo "Copying scripts..."
dos2unix ./$SCRIPTNAME.py
echo "--removed windows cr:lf $SCRIPTNAME.py"
dos2unix ./$SCRIPTNAME.sh
echo "--removed windows cr:lf $SCRIPTNAME.sh"
chmod 755 ./$SCRIPTNAME.py
echo "--adjusted permissions $SCRIPTNAME.py"
chmod 755 ./$SCRIPTNAME.sh
echo "--adjusted permissions $SCRIPTNAME.sh"
cp ./$SCRIPTNAME.sh /etc/init.d
echo "--copied $SCRIPTNAME.sh to /etc/init.d"
mkdir /usr/local/bin/$SCRIPTNAME
cp ./blinktemp.py /usr/local/bin/$SCRIPTNAME
echo "--copied $SCRIPTNAME.py to /usr/local/bin/$SCRIPTNAME"
chmod 755 /etc/init.d/$SCRIPTNAME.sh
echo "--adjusted permissions $SCRIPTNAME.sh"
update-rc.d $SCRIPTNAME.sh defaults
echo "--service $SCRIPTNAME installed"
/etc/init.d/$SCRIPTNAME.sh start