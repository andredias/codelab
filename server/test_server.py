from .server import app

# see: http://flask.pocoo.org/docs/0.10/testing/


class TestCodeLab(object):

    def setup(self):
        app.config['TESTING'] = True
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
