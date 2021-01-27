from flask import json
from whack_a_bug_api.tests.test_baseCase import BaseCase
from whack_a_bug_api.models.projects import Project
from whack_a_bug_api.models.users import User
from whack_a_bug_api.db import db
from whack_a_bug_api.models.pivots import project_user_table


class ProjectTests(BaseCase):
    """Project test units"""
    
    def test_lead_role_user_can_create_project(self):
        self.register_user('Juniper', 'Lee', 'lee.juniper@example.com', 3)
        
        with self.client:
            login = self.login_user('lee.juniper@example.com')
            data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(data['access_token'])
            }
            project = self.create_project(headers)
            data = json.loads(project.data.decode())

            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Project created successfully!')
            self.assertEqual(project.status_code, 201)
            self.assertIn('Food Blog', data['data']['title'])

    def test_other_roles_cannot_create_project(self):
        self.register_user('Jennifer', 'Lee', 'lee.jennifer@example.com', 2)
        
        with self.client:
            login = self.login_user('lee.jennifer@example.com')
            data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(data['access_token'])
            }
            project = self.create_project(headers)
            data = json.loads(project.data.decode())

            self.assertTrue(data['message'] == 'You do not have access to this action!')
            self.assertEqual(project.status_code, 403)
            
    def test_api_gets_all_projects(self):
        self.register_user('Juniper', 'Lee', 'lee.juniper@example.com', 3)
        
        with self.client:
            login = self.login_user('lee.juniper@example.com')
            data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(data['access_token'])
            }
            
            res = self.create_project(headers)
            self.assertEqual(res.status_code, 201)
            
            resp = self.client.get('/api/main/projects', headers = headers)
            data = json.loads(resp.data.decode())
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Food Blog', data['data'][0]['title'])
            
            
    def test_project_can_be_updated(self):
        self.register_user('Juniper', 'Lee', 'lee.juniper@example.com', 3)
        
        with self.client:
            login = self.login_user('lee.juniper@example.com')
            data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(data['access_token'])
            }
            self.create_project(headers)
            
            update_project = {'title': 'Fashion Blog Design'}
            res = self.client.put('/api/main/projects/project/1', data = json.dumps(update_project), headers = headers)
            result = json.loads(res.data.decode())
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('Fashion', result['data']['title'])
    
    
    def test_api_can_get_project_by_id(self):
        self.register_user('Juniper', 'Lee', 'lee.juniper@example.com', 3)
        
        with self.client:
            login = self.login_user('lee.juniper@example.com')
            data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(data['access_token'])
            }
            self.create_project(headers)
            
            res = self.client.get('/api/main/projects/project/1', headers = headers)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Food Blog', str(res.data))
            
            
    def test_api_can_delete_projects(self):
        self.register_user('Juniper', 'Lee', 'lee.juniper@example.com', 3)
        
        existing_project1 = Project(title = 'Food Blog Design')
        existing_project2 = Project(title = 'Ticketing System')
        existing_project3 = Project(title = 'Mobile app development')
        existing_project1.save()
        existing_project2.save()
        existing_project3.save()
        
        with self.client:
            login = self.login_user('lee.juniper@example.com')
            data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(data['access_token'])
            }
            
            res = self.client.delete('/api/main/projects', data = json.dumps(dict(selectedIDs = [2])), headers = headers)
            data = json.loads(res.data.decode())
            
            self.assertEqual(res.status_code, 202)
            self.assertTrue(data['message'] == 'Project(s) deleted Successfully!')
            
            #check if project still exists
            resp = self.client.get('/api/main/projects/project/2', headers = headers)
            self.assertEqual(resp.status_code, 404)
            
    def test_project_already_exists(self):
        self.register_user('Juniper', 'Lee', 'lee.juniper@example.com', 3)
        
        with self.client:
            login = self.login_user('lee.juniper@example.com')
            data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(data['access_token'])
            }
            
            res = self.create_project(headers)
            resp = self.create_project(headers)
            data = json.loads(resp.data.decode())
        
            self.assertTrue(data['message'] == 'Project already exists!')
            self.assertEqual(resp.status_code, 409)
            
    def test_lead_can_assign_users_to_project(self):
        self.register_user('Juniper', 'Lee', 'lee.juniper@example.com', 3)
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
            first_name = 'Michelle',
            last_name = 'Pfieffer',
            email = 'pfieffer.michelle@example.com',
            password = 'Hot100x'
        )
        user4 = User(
            first_name = 'Kwaghbee',
            last_name = 'Rissa',
            email = 'rissa.kwaghbee@example.com',
            password = 'Brokenheart1'
        )
        user5 = User(
            first_name = 'Naruto',
            last_name = 'Uzumaki',
            email = 'uzumaki.naruto@example.com',
            password = 'Rasengan1'
        )
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.add(user4)
        db.session.add(user5)
        db.session.commit()
        
        with self.client:
            login = self.login_user('lee.juniper@example.com')
            login_data = json.loads(login.data.decode())
            
            headers = headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(login_data['access_token'])
            }
            
            resp = self.client.post('/api/main/projects', data = json.dumps(dict(
                title = 'Food Blog Design',
                users = [1, 3 , 5]
            )), headers = headers)
            
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Project created successfully!')
            self.assertEqual(resp.status_code, 201)
            self.assertIn('Food Blog Design', data['data']['title'])
            
            link = db.session.query(project_user_table).all()
            if link:
                self.assertEqual(link[1].user_id, user2.id)
            