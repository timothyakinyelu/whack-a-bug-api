from flask import json
from whack_a_bug_api.tests.baseCase import BaseCase
from whack_a_bug_api.models.projects import Project
from whack_a_bug_api.models.users import User


class ProjectTests(BaseCase):
    """Project test units"""
    
    def test_authenticated_user_can_create_project(self):
        self.register_user()
        
        with self.client:
            login = self.login_user()
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
            
    def test_api_gets_all_projects(self):
        self.register_user()
        
        with self.client:
            login = self.login_user()
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
        self.register_user()
        
        with self.client:
            login = self.login_user()
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
        self.register_user()
        
        with self.client:
            login = self.login_user()
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
        self.register_user()
        
        existing_project1 = Project(title = 'Food Blog Design')
        existing_project2 = Project(title = 'Ticketing System')
        existing_project3 = Project(title = 'Mobile app development')
        existing_project1.save()
        existing_project2.save()
        existing_project3.save()
        
        with self.client:
            login = self.login_user()
            data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(data['access_token'])
            }
            
            res = self.client.delete('/api/main/projects', data = json.dumps(dict(selectedIDs = [2])), headers = headers)
            data = json.loads(res.data.decode())
            
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['message'] == 'Project(s) deleted Successfully!')
            
            #check if project still exists
            resp = self.client.get('/api/main/projects/project/2', headers = headers)
            self.assertEqual(resp.status_code, 404)
            
    def test_project_already_exists(self):
        self.register_user()
        
        with self.client:
            login = self.login_user()
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