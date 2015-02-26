from flask import url_for
from .server import app, mail

# see: http://flask.pocoo.org/docs/0.10/testing/


class TestCodeLab(object):

    def setup(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        mail.state.suppress = True  # gambiarra??
        self.app = app.test_client()

    # def tearDown(self):
    #     os.close(self.db_fd)
    #     os.unlink(codelab.app.config['DATABASE'])

    def test_landing(self):
        rv = self.app.get('/')
        assert 'Code Lab' in str(rv.data)
        assert 'Python' in str(rv.data)

    def test_new_project(self):
        rv = self.app.get('/project/new/python')
        assert '<span>Run</span>' in str(rv.data)

    def test_contact(self):
        '''
        see: https://pythonhosted.org/Flask-Mail/#unit-tests-and-suppressing-emails
        '''
        rv = self.app.get('/contact')
        assert '<form name="contact_form">' in str(rv.data)
        assert 'subject' in str(rv.data)
        with mail.record_messages() as outbox:
            rv = self.app.post('/contact', data=dict(subject='teste', email='teste@teste',
                                                     description='descrição'))
            assert len(outbox) == 0
            assert '<div class="error">' in str(rv.data)
        with mail.record_messages() as outbox:
            rv = self.app.post('/contact', data=dict(type_='bug', subject='testing contact form',
                                                     name='tester', email='test@gmail.com',
                                                     description='this is a test\nLâmpada, Açúcar'))
            assert 'Your message was sent successfully!' in str(rv.data)
            assert len(outbox) == 1
            assert outbox[0].subject == 'bug: testing contact form'

    def test_pt_br(self):
        with app.test_request_context():
            app.config['BABEL_DEFAULT_LOCALE'] = 'pt_BR'
            rv = app.test_client().get('/')
            assert '<span>Execute</span>, <span>melhore</span>' in str(rv.data)

    def test_en_us(self):
        with app.test_request_context():
            app.config['BABEL_DEFAULT_LOCALE'] = 'en_US'
            rv = app.test_client().get('/')
            assert '<span>Run</span>, <span>improve</span>' in str(rv.data)

    def test_faq(self):
        resp = self.app.get('/help/faq')
        assert resp.status_code == 200

    def test_terms(self):
        resp = self.app.get('/help/terms_of_use')
        assert resp.status_code == 200

    def test_dojo(self):
        languages = ('python', 'c', 'c++', 'ruby', 'javascript', 'go')
        with app.test_request_context():
            for language in languages:
                resp = self.app.get(url_for('dojo', language=language))
                assert resp.status_code == 200
                assert '<span>%s</span>' % language in str(resp.data)

    def test_samples_page(self):
        resp = self.app.get('/samples')
        data = str(resp.data)
        assert resp.status_code == 200
        assert data.count('Hello, world!') >= 6  # one for each language at least
        assert 'Python' in data

    def test_last_visited(self):
        resp = self.app.get('/visited?option=last_visited')
        assert resp.status_code == 200

    def test_most_visited(self):
        resp = self.app.get('/visited?option=most_visited')
        assert resp.status_code == 200
