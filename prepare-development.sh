#!/bin/bash
# apt-get install -y nodejs npm
# npm install -g gulp
source `which virtualenvwrapper.sh`
mkvirtualenv codelab -p `which python3`
pip3 install -r requirements.txt
npm install

# http://askubuntu.com/questions/488529/pyvenv-3-4-error-returned-non-zero-exit-status-1
# pyvenv-3 --without-pip venv
# source venv/bin/activate
# curl https://bootstrap.pypa.io/get-pip.py | python
# deactivate
# source venv/bin/activate
# pip install -r requirements.txt