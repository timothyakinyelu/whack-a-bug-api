from flask_testing import TestCase
from whack_a_bug_api.helpers.load_config import loadConfig
from whack_a_bug_api.db import db
from whack_a_bug_api import createApp

app = createApp()


class BaseCase(TestCase):
    """ Parent class for test cases"""
    
    def create_app(self):
        mode = 'testing'
        Config = loadConfig(mode)
        app.config.from_object(Config)
        
        return app
    
    def setUp(self):
        db.create_all()
        
    def tearDown(self):
        """ Teardown all initialized variables and tables"""
        
        with self.app.app_context():
            db.session.remove()
            db.drop_all()