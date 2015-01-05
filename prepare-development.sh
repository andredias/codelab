#!/bin/bash
source `which virtualenvwrapper.sh`
mkvirtualenv codebox -p `which python3`
pip install -r requirements.txt
npm install
gulp

