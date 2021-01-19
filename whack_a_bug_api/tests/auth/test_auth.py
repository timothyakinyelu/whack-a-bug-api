from whack_a_bug_api.tests.baseCase import BaseCase
from flask import json
from whack_a_bug_api.models.users import User
from whack_a_bug_api.db import db


class AuthenticationTests(BaseCase):
    """Test all authentication routes"""
    
    def test_user_can_be_registered(self):
        self.user = {
            'first_name': 'Juniper',
            'last_name': 'Lee',
            'email': 'lee.juniper@example.com',
            'password': 'Jumper1'
        }
        
        with self.client:
            res = self.client.post('/api/auth/register', data = json.dumps(self.user), content_type = 'application/json')
            data = json.loads(res.data.decode())
            
            self.assertEqual(res.status_code, 201)
            self.assertEqual(data['message'], 'User registered successfully!')
            
    def test_user_already_exists(self):
        self.user = {
            'first_name': 'Juniper',
            'last_name': 'Lee',
            'email': 'lee.juniper@example.com',
            'password': 'Jumper1'
        }
        
        with self.client:
            res = self.client.post('/api/auth/register', data = json.dumps(self.user), content_type = 'application/json')
            self.assertEqual(res.status_code, 201)
            
            try:
                resp = self.client.post('/api/auth/register', data = json.dumps(self.user), content_type = 'application/json')
                data = json.loads(resp.data.decode())
            except AssertionError as a:
                self.assertEqual(str(a), 'This username already exists!')
        
                
    def test_token_can_be_generated(self):
        user = User(
            first_name = 'Juniper',
            last_name = 'Lee',
            email = 'lee.juniper@example.com',
            password = 'Jumper1'
        )
        db.session.add(user)
        db.session.commit()
        
        auth_token = user.generate_token(user.public_id)
        try:
            self.assertTrue(type(auth_token), bytes)
        except Exception as exe:
            print(exe)
            
            
    def test_user_can_login(self): 
        self.new_user = {
            'first_name': 'Juniper',
            'last_name': 'Lee',
            'email': 'lee.juniper@example.com',
            'password': 'Jumper1'
        }
        
        self.user = {
            'email': 'lee.juniper@example.com',
            'password': 'Jumper1'
        }
        
        with self.client:
            register = self.client.post('/api/auth/register', data = json.dumps(self.new_user), content_type = 'application/json')
            
            login = self.client.post('/api/auth/login', data = json.dumps(self.user), content_type = 'application/json')
            data = json.loads(login.data.decode())
            
            self.assertEqual(login.status_code, 200)
            self.assertEqual(data['message'], 'Login Successful!')
            self.assertTrue(data['access_token'])
            
    def test_unregistered_user_cannot_login(self):
        self.user = {
            'email': 'lee.juniper@example.com',
            'password': 'Jumper1'
        }
        
        with self.client:
            login = self.client.post('/api/auth/login', data = json.dumps(self.user), content_type = 'application/json')
            data = json.loads(login.data.decode())
            
            self.assertEqual(login.status_code, 402)
            self.assertEqual(data['message'], 'email or password does not exist!')
            
    def test_email_is_valid_email_address(self):
        self.new_user = {
            'first_name': 'Juniper',
            'last_name': 'Lee',
            'email': 'lee.juniper',
            'password': 'Jumper1'
        }
        
        with self.client:
            try:
                register = self.client.post('/api/auth/register', data = json.dumps(self.new_user), content_type = 'application/json')
            except AssertionError as e:
                self.assertEqual(str(e), 'Provided entry is not an email address')