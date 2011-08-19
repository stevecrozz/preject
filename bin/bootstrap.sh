#!/bin/sh

sudo easy_install virtualenv
sudo easy_install virtualenvwrapper
echo "/usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
. ~/.bashrc
