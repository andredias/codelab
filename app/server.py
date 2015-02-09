#!/usr/bin/python3

import sh
import json
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, render_template, request, url_for
from flask.ext.script import Manager
from flask.ext.mail import Mail, Message
from flask.ext.babel import Babel


CONTAINER = 'codelab'


app = Flask(__name__)
app.config.from_object('app.config')
app.config.from_object('app.non_versioned_config')
app.jinja_env.add_extension('jinja2.ext.do')
manager = Manager(app)
mail = Mail(app)
mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                           'codelab@pronus.io',
                           app.config['MAIL_RECEIVER'],
                           '{} Error'.format(app.config['APP_NAME']),
                           (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),)
mail_handler.setLevel(logging.ERROR)
app.logger.addHandler(mail_handler)
handler = RotatingFileHandler('/tmp/%s.log' % CONTAINER, maxBytes=100000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
babel = Babel(app)


@babel.localeselector
def get_locale():
    # try to guess the language from the user accept
    # header the browser transmits.
    return request.accept_languages.best_match(['pt_BR', 'en'])


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
    output = sh.docker.run('-i', '--rm', '--net', 'none', CONTAINER, _ok_code=[0, 1, 2],
                           _in=params_json)
    app.logger.info(output)
    return output.stdout.decode('utf-8')


from .forms import ContactForm
from .decorators import async


@async
def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Zoho mail does not allow to use a sender who is not at @pronus.io
        message = Message(
            subject='{0}: {1}'.format(form.type_.data, form.subject.data),
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=app.config['MAIL_RECEIVER'],
            body='from: %s <%s>\n\n%s' % (form.name.data, form.email.data, form.description.data),
        )
        send_async_mail(app, message)
        return render_template('message_sent.html')
    return render_template('contact_form.html', form=form)


@app.route('/help/<topic>')
def help(topic):
    return render_template(topic + '.html')
