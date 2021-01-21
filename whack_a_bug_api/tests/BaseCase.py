from flask_testing import TestCase
from whack_a_bug_api.helpers.load_config import loadConfig
from whack_a_bug_api.db import db
from whack_a_bug_api import createApp
from flask import json

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
            
    def register_user(self):
        """create new user for test cases"""
        
        self.user = {
            'first_name': 'Juniper',
            'last_name': 'Lee',
            'email': 'lee.juniper@example.com',
            'password': 'Jumper1'
        }
        
        response = self.client.post('/api/auth/register', data = json.dumps(self.user), content_type = 'application/json')
        return response
    
    def login_user(self):
        """login a test case user"""
        
        self.user = {
            'email': 'lee.juniper@example.com',
            'password': 'Jumper1'
        }
        
        response = self.client.post('/api/auth/login', data = json.dumps(self.user), content_type = 'application/json')
        return response
    
    def create_project(self, headers):
        """create a test case project"""
        
        self.project = {'title': 'Food Blog Design'}
        
        response = self.client.post('/api/main/projects', data = json.dumps(self.project), headers = headers)
        return response