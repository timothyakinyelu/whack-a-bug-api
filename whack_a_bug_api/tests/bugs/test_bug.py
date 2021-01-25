from flask import json
from whack_a_bug_api.tests.baseCase import BaseCase
from whack_a_bug_api.models.projects import Project
from whack_a_bug_api.models.users import User
from whack_a_bug_api.models.bugs import Bug
from whack_a_bug_api.db import db

class BugTests(BaseCase):
    """Bug issue test units"""
    
    def create_bug(self, headers):
        self.bug = {
            'title': 'Unable to login',
            'project_name': 'Food Blog Design'
        }
        
        response = self.client.post('/api/main/bugs', data = json.dumps(self.bug), headers = headers)
        return response
        
    def test_bug_issue_can_be_created(self):
        self.register_user()
        
        with self.client:
            login = self.login_user()
            login_data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(login_data['access_token'])
            }
            
            self.create_project(headers)
            
            res = self.create_bug(headers)
            data = json.loads(res.data.decode())
            
            self.assertEqual(res.status_code, 201)
            self.assertIn('Unable to login', data['data']['title'])
            self.assertIn('WB1001', data['data']['ticket_ref'])
            self.assertTrue(data['message'] == 'Bug Issue created successfully!')
            
            
    def test_all_issues_can_be_fetched(self):
        self.register_user()
        
        with self.client:
            login = self.login_user()
            login_data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(login_data['access_token'])
            }
            
            self.create_project(headers)
            
            res = self.create_bug(headers)
            
            resp = self.client.get('/api/main/bugs', headers = headers)
            data = json.loads(resp.data.decode())
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('WB1001', data['data'][0]['ticket_ref'])
            
    def test_api_can_fetch_issue_by_id(self):
        self.register_user()
        
        with self.client:
            login = self.login_user()
            login_data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(login_data['access_token'])
            }
            
            self.create_project(headers)
            
            res = self.create_bug(headers)
            
            res = self.client.get('/api/main/bugs/1', headers = headers)
            data = json.loads(res.data.decode())
            
            self.assertEqual('Unable to login', data['data']['title'])
            self.assertEqual(res.status_code, 200)
            
    def test_issue_can_be_assigned_to_user(self):
        self.register_user()
        
        user1 = User(
            first_name = 'Jane',
            last_name = 'Fonda',
            email = 'fonda.jane@example.com',
            password = 'Rocky12'
        )
        user2 = User(
            first_name = 'Luke',
            last_name = 'Skywalker',
            email = 'skywalker.luke@example.com',
            password = 'Darthfather1'
        )
        user3 = User(
            first_name = 'Naruto',
            last_name = 'Uzumaki',
            email = 'uzumaki.naruto@example.com',
            password = 'Rasengan1'
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
        
        with self.client:
            login = self.login_user()
            login_data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(login_data['access_token'])
            }
            
            self.client.post('/api/main/projects', data = json.dumps(dict(
                title = 'Food Blog Design',
                users = [2, 3]
            )), headers = headers)
            
            self.client.post('/api/main/projects', data = json.dumps(dict(
                title = 'Fashion Blog Design',
                users = [3]
            )), headers = headers)
            self.create_bug(headers)
            
            resp = self.client.put('/api/main/bugs/1', data = json.dumps(dict(
                userID = 2,
                projectID = 1
            )), headers = headers)
            data = json.loads(resp.data.decode())
            
            self.assertEqual(resp.status_code, 200)
            
            res = self.client.get('/api/main/bugs/1', headers = headers)
            data = json.loads(res.data.decode())
            
            self.assertEqual('Unable to login', data['data']['title'])
            self.assertTrue(data['data']['assigned_to'] == 2)
            
    def test_bug_status_can_be_updated(self):
        self.register_user()
        
        with self.client:
            login = self.login_user()   
            login_data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(login_data['access_token'])
            }
            
            self.create_project(headers)
            self.create_bug(headers)
            resp = self.client.put('/api/main/bugs/1', data = json.dumps(dict(
                bugStatus = 'Ongoing',
                projectID = 1
            )), headers = headers)
            data = json.loads(resp.data.decode())
            
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(data['message'] == 'Bug issue updated successfully!')
            
            res = self.client.get('/api/main/bugs/1', headers = headers)
            data = json.loads(res.data.decode())
            
            self.assertEqual('Unable to login', data['data']['title'])
            self.assertTrue(data['data']['bug_status'] == 'Ongoing')
            
    def test_test_status_can_be_updated(self):
        self.register_user()
            
        with self.client:
            login = self.login_user()   
            login_data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(login_data['access_token'])
            }
            
            self.create_project(headers)
            self.create_bug(headers)
            resp = self.client.put('/api/main/bugs/1', data = json.dumps(dict(
                bugStatus = 'Awaiting Test',
                projectID = 1
            )), headers = headers)
            data = json.loads(resp.data.decode())
            
            self.assertEqual(resp.status_code, 200)
            self.assertTrue(data['message'] == 'Bug issue updated successfully!')
            
            res = self.client.get('/api/main/bugs/1', headers = headers)
            data = json.loads(res.data.decode())
            
            self.assertEqual('Unable to login', data['data']['title'])
            self.assertTrue(data['data']['bug_status'] == 'Awaiting Test')
            self.assertTrue(data['data']['test_status'] == 'Pending')