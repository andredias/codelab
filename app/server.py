#!/usr/bin/python3

import logging
from datetime import timedelta
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, url_for, abort, redirect
from flask.ext.script import Manager
from flask.ext.mail import Mail, Message
from flask.ext.moment import Moment
from flask.ext.babel import Babel
from flask.ext.webcache import easy_setup
from flask.ext.webcache.modifiers import cache_for
from werkzeug.contrib.cache import RedisCache
from .mail_handler import MailHandler
from .forms import ContactForm
from .decorators import async
from .projects import (
    pygmentize, last_visited, most_visited, count_visit, cache_project,
    get_project_to_run
)


app = Flask(__name__)
app.config.from_object('app.config')
app.config.from_object('app.non_versioned_config')
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.globals.update(pygmentize=pygmentize)
manager = Manager(app)
mail = Mail(app)
moment = Moment(app)

cache = RedisCache(app.config['CACHE_REDIS_HOST'])
easy_setup(app, cache)


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
handler = RotatingFileHandler('/tmp/%s.log' % '_'.join(app.config['APP_NAME'].lower().split()),
                              maxBytes=(2 ** 20))
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

app.jinja_env.globals.update(get_locale=get_locale)


@app.route('/project/new/<language>')
def dojo(language):
    language = language.lower()
    return render_template('dojo.html', language=app.config['LANGUAGES'][language]['label'],
                           lint_data=[])


@app.route('/project/<id>')
@count_visit(cache=cache)
@cache_for(days=1)
def project_page(id):
    project = cache.get(id)
    if not project:
        abort(404)
    output_data = ''
    for key in ('compilation', 'build', 'execution', 'run'):
        if key not in project:
            continue
        output_data += '%s%s' % (project[key].get('stdout', ''),
                                 project[key].get('stderr', ''))
    lint_data = list(project['lint'].values())[0] if project.get('lint') else []
    return render_template('dojo.html',
                           title=project.get('title'),
                           description=project.get('description', ''),
                           input_data=project.get('input', ''),
                           source=project['source'],
                           language=app.config['LANGUAGES'][project['language']]['label'],
                           lint_data=lint_data,
                           output_data=output_data)


@app.route('/_do_the_thing', methods=['POST'])
def do_the_thing():
    project = get_project_to_run(request.form)
    destination = url_for('project_page', id=project['id'])
    if not cache.get(project['id']):
        cache_project(cache, project, timeout=int(timedelta(days=180).total_seconds()))
        app.logger.info('NOT CACHED:\n\tparams: %s' % project)
    else:
        app.logger.info('Cached: %s' % destination)
    return redirect(destination)


@app.route('/')
@cache_for(hours=1)
def landing():
    from .projects import get_samples
    samples = get_samples(cache, app.config['LANGUAGES'].keys())
    return render_template('landing_page.html', projects=samples)


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
@cache_for(days=7)
def help(topic):
    return render_template(topic + '.html')


@app.route('/samples')
@cache_for(days=60)
def examples():
    from .projects import get_samples
    languages = app.config['LANGUAGES'].keys()
    samples = get_samples(cache, app.config['LANGUAGES'].keys())
    return render_template('snippets.html',
                           languages=languages,
                           projects=samples)


@app.route('/visited')
def visited():
    option = request.args['option']
    languages = app.config['LANGUAGES'].keys()
    if option == 'last_visited':
        projects = last_visited(cache, languages)
    else:
        projects = most_visited(cache, languages)
    return render_template('fill_project.html', projects=projects)
