#!/usr/bin/python3

import sh
import json
import logging
from redis import Redis
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, url_for, abort, redirect
from flask.ext.script import Manager
from flask.ext.mail import Mail, Message
from flask.ext.babel import Babel
from hashlib import md5
from .mail_handler import MailHandler
from .forms import ContactForm
from .decorators import async


CONTAINER = 'codelab'


app = Flask(__name__)
app.config.from_object('app.config')
app.config.from_object('app.non_versioned_config')
app.jinja_env.add_extension('jinja2.ext.do')
manager = Manager(app)
mail = Mail(app)

redis = Redis(app.config['REDIS_HOST'])


@async
def send_async_mail(msg):
    with app.app_context():
        mail.send(msg)


mail_handler = MailHandler(
    send_async_mail,
    subject='{} Error'.format(app.config['APP_NAME']),
    sender=app.config['MAIL_DEFAULT_SENDER'],
    recipients=app.config['MAIL_RECEIVERS'])
mail_handler.setLevel(logging.ERROR)
mail_handler.setFormatter(logging.Formatter('''
Message type: %(levelname)s
Location:     %(pathname)s:%(lineno)d
Module:       %(module)s
Function:     %(funcName)s
Time:         %(asctime)s

Message:

%(message)s
'''))
app.logger.addHandler(mail_handler)
handler = RotatingFileHandler('/tmp/%s.log' % CONTAINER, maxBytes=1000000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)
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
    return render_template('dojo.html', language=language, lint_data=[])


@app.route('/project/<id>')
def project_page(id):
    project = redis.hgetall(id)
    if not project:
        abort(404)
    params = json.loads(project[b'params'].decode('utf-8'))
    output = json.loads(project[b'output'].decode('utf-8'))
    lint_data = output.get('lint', [])
    output_data = ''
    if output.get('compilation'):
        output_data += '%s%s' % (output['compilation'].get('stdout', ''),
                                 output['compilation'].get('stderr', ''))
    if output.get('execution'):
        output_data += '%s%s' % (output['execution'].get('stdout', ''),
                                 output['execution'].get('stderr', ''))
    return render_template('dojo.html',
                           input_data=params['input'],
                           source=params['source'],
                           language=params['language'],
                           lint_data=lint_data,
                           output_data=output_data)


def run(params_json):
    return sh.docker.run('-i', '--rm', '--net', 'none', CONTAINER, _ok_code=[0, 1, 2],
                         _in=params_json)


@app.route('/_do_the_thing', methods=['POST'])
def do_the_thing():
    params = {'input': request.form['input'], 'source': request.form['source'],
              'language': request.form['language']}
    id = md5('{input}{source}{language}'.format(**params).encode('utf-8')).hexdigest()
    destination = url_for('project_page', id=id)
    if not redis.exists(id):
        params_json = json.dumps(params)
        output_json = run(params_json)
        redis.hmset(id, {'params': params_json, 'output': output_json})
        app.logger.info('NOT CACHED:\n\tparams: %s\n\toutput: %s' % (params_json, output_json))
    else:
        app.logger.info('Cached: %s' % destination)
    return redirect(destination)


@app.route('/')
def landing():
    languages = (
        ('Python (3)', url_for('static', filename='images/python.svg')),
        ('C', url_for('static', filename='images/c.svg')),
        ('C++', url_for('static', filename='images/cpp.svg')),
        ('Go', url_for('static', filename='images/go.png')),
        ('Javascript (Node.js)', url_for('static', filename='images/javascript.png')),
        ('Ruby', url_for('static', filename='images/ruby.svg')),
    )
    return render_template('landing_page.html', languages=languages)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Zoho mail does not allow to use a sender who is not at @pronus.io
        message = Message(
            subject='{0}: {1}'.format(form.type_.data, form.subject.data),
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=app.config['MAIL_RECEIVERS'],
            body='from: %s <%s>\n\n%s' % (form.name.data, form.email.data, form.description.data),
        )
        send_async_mail(message)
        return render_template('message_sent.html')
    return render_template('contact_form.html', form=form)


@app.route('/help/<topic>')
def help(topic):
    return render_template(topic + '.html')
