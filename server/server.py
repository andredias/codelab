#!/usr/bin/python3

import sh
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request
from flask.ext.script import Manager

codebox = sh.docker.run.bake('-i', '--rm', '--net', 'none', 'codebox', _ok_code=[0, 1, 2])

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/_do_the_thing')
def do_the_thing():
    language = request.args.get('language', 'python')
    source = request.args.get('code')
    _input = request.args.get('input')
    params = {'input': _input, 'source': source, 'language': language}
    params_json = json.dumps(params)
    app.logger.info(params_json)
    output = codebox(_in=params_json)
    app.logger.info(output)
    return output.stdout.decode('utf-8')


if __name__ == '__main__':
    handler = RotatingFileHandler('/tmp/codebox.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    manager.run()
