#!/usr/bin/python3

import sh
import json
from flask import Flask, render_template, request, url_for
from flask.ext.script import Manager
from flask.ext.mail import Mail, Message


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.from_pyfile('non_versioned_config.py')
app.jinja_env.add_extension('jinja2.ext.do')
manager = Manager(app)
mail = Mail(app)


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
    output = sh.docker.run('-i', '--rm', '--net', 'none', 'codebox', _ok_code=[0, 1, 2],
                           _in=params_json)
    app.logger.info(output)
    return output.stdout.decode('utf-8')


from .model import ContactForm
from .decorators import async


@async
def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = Message(
            subject='codelab:{0}: {1}'.format(form.type_.data, form.subject.data),
            sender=(form.name.data, form.email.data),
            recipients=['suporte@pronus.eng.br'],
            body=form.description.data,
        )
        send_async_mail(app, message)
        return render_template('message_sent.html')
    return render_template('contact_form.html', form=form)


@app.route('/help/<topic>')
def help(topic):
    return render_template(topic + '.html')
