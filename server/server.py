#!/usr/bin/python3

import sh
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, url_for
from flask.ext.script import Manager

codebox = sh.docker.run.bake('-i', '--rm', '--net', 'none', 'codebox', _ok_code=[0, 1, 2])

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def index():
    languages = (
        ('Python', url_for('static', filename='images/python.svg')),
        ('C', url_for('static', filename='images/c.svg')),
        ('C++', url_for('static', filename='images/cpp.svg')),
        ('Go', url_for('static', filename='images/go.png')),
        ('Javascript', url_for('static', filename='images/javascript.png')),
        ('Ruby', url_for('static', filename='images/ruby.svg')),
    )
    return render_template('landing_page.html', languages=languages)


@app.route('/dojo/<language>')
def dojo(language):
    language = language.lower()
    ace_mode_map = {
        'c': 'c_cpp',
        'c++': 'c_cpp',
        'c#': 'csharp',
        'go': 'golang',
    }
    ace_mode = 'ace/mode/' + ace_mode_map.get(language, language)
    ace_theme = 'ace/theme/cobalt'
    return render_template('dojo.html', language=language, ace_mode=ace_mode, ace_theme=ace_theme)


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
