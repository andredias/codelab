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
            assert outbox[0].subject == 'codelab:bug: testing contact form'
