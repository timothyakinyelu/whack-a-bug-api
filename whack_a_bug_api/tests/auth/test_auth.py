from whack_a_bug_api.tests.baseCase import BaseCase
from flask import json


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
            res = self.client.post('/api/auth/users', data = json.dumps(self.user), content_type = 'application/json')
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
            res = self.client.post('/api/auth/users', data = json.dumps(self.user), content_type = 'application/json')
            self.assertEqual(res.status_code, 201)
            
            with self.assertRaises(AssertionError):
                resp = self.client.post('/api/auth/users', data = json.dumps(self.user), content_type = 'application/json')
                data = json.loads(resp.data.decode())