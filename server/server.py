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


@app.route('/project/new/<language>')
def dojo(language):
    # projeto = project_or_new(session['project_id'])
    language = language.lower()
    ace_theme = 'ace/theme/cobalt'
    languages = {  # name: mode
        'python': 'python',
        'c': 'c_cpp',
        'c++': 'c_cpp',
        'go': 'golang',
        'javascript': 'javascript',
        'ruby': 'ruby',
    }
    return render_template('dojo.html', languages=languages, language=language, ace_theme=ace_theme)


@app.route('/')
def landing():
    languages = (
        ('Python', url_for('static', filename='images/python.svg')),
        ('C', url_for('static', filename='images/c.svg')),
        ('C++', url_for('static', filename='images/cpp.svg')),
        ('Go', url_for('static', filename='images/go.png')),
        ('Javascript', url_for('static', filename='images/javascript.png')),
        ('Ruby', url_for('static', filename='images/ruby.svg')),
    )
    return render_template('landing_page.html', languages=languages)


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


from model import ContactForm


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # enviar e-mail
        return render_template('message_sent.html')
    app.logger.info(request)
    return render_template('contact_form.html', form=form)


@app.route('/help/<topic>')
def help(topic):
    return render_template(topic + '.html')

WTF_CSRF_SECRET_KEY = app.secret_key = b'\xf06\xe34\x93\xf0\xad\xa5\xe7\xde\xf1R' \
                                       b'\xb3\xef\xd9\xaa\x92J\x14\xea'

if __name__ == '__main__':
    handler = RotatingFileHandler('/tmp/codebox.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    manager.run()
