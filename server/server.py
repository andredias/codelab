#!/usr/bin/python3

import sh
import json

from flask import Flask, render_template, jsonify, request
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
    params = {'_input': _input, 'source': source, 'language': language}
    output = codebox(_in=json.dumps(params))
    stdout = output.stdout.decode('utf-8')
    stderr = output.stderr.decode('utf-8')
    return jsonify(stdout=stdout, stderr=stderr)

if __name__ == '__main__':
    manager.run()