from flask import json
from whack_a_bug_api.tests.baseCase import BaseCase
from whack_a_bug_api.models.projects import Project
from whack_a_bug_api.models.users import User


class ProjectTests(BaseCase):
    
    def test_authenticated_user_can_create_project(self):
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
        
        self.project = {'title': 'Food Blog Design'}
        
        with self.client:
            register = self.client.post('/api/auth/register', data = json.dumps(self.new_user), content_type = 'application/json')
            
            user = User.query.all()
            print(user[0].public_id)
            
            login = self.client.post('/api/auth/login', data = json.dumps(self.user), content_type = 'application/json')
            data = json.loads(login.data.decode())
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(data['access_token'])
            }
            project = self.client.post('/api/main/projects', data = json.dumps(self.project), headers = headers)
            data = json.loads(project.data.decode())

            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Project created successfully!')
            self.assertEqual(project.status_code, 201)
            self.assertIn('Food Blog', data['data']['title'])
            
    def test_api_gets_all_projects(self):
        self.project = {'title': 'Food Blog Design'}
        
        with self.client:
            res = self.client.post('/api/main/projects', data = json.dumps(self.project), content_type = 'application/json')
            self.assertEqual(res.status_code, 201)
            
            resp = self.client.get('/api/main/projects')
            data = json.loads(resp.data.decode())
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Food Blog', data['data'][0]['title'])
            
            
    def test_project_can_be_updated(self):
        existing_project1 = Project(title = 'Food Blog Design')
        existing_project2 = Project(title = 'Ticketing System')
        existing_project1.save()
        existing_project2.save()
        
        self.project = {'title': 'Fashion Blog Design'}
        
        
        with self.client:
            res = self.client.put('/api/main/projects/project/1', data = json.dumps(self.project), content_type = 'application/json')
            data = json.loads(res.data.decode())
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('Fashion', data['data']['title'])
    
    
    def test_api_can_get_project_by_id(self):
        existing_project1 = Project(title = 'Food Blog Design')
        existing_project2 = Project(title = 'Ticketing System')
        existing_project1.save()
        existing_project2.save()
        
        with self.client:
            res = self.client.get('/api/main/projects/project/2')
            self.assertEqual(res.status_code, 200)
            self.assertIn('Ticketing', str(res.data))
            
            
    def test_api_can_delete_projects(self):
        existing_project1 = Project(title = 'Food Blog Design')
        existing_project2 = Project(title = 'Ticketing System')
        existing_project3 = Project(title = 'Mobile app development')
        existing_project1.save()
        existing_project2.save()
        existing_project3.save()
        
        with self.client:
            res = self.client.delete('/api/main/projects', data = json.dumps(dict(selectedIDs = [2])), content_type = 'application/json')
            data = json.loads(res.data.decode())
            
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['message'] == 'Project(s) deleted Successfully!')
            
            #check if project still exists
            resp = self.client.get('/api/main/projects/project/2')
            self.assertEqual(resp.status_code, 404)
            
    def test_project_already_exists(self):
        existing_project = Project(title = 'Food Blog Design')
        existing_project.save()
        
        self.project = {'title': 'Food Blog Design'}
        
        with self.client:
            res = self.client.post('/api/main/projects', data = json.dumps(self.project), content_type = 'application/json')
            data = json.loads(res.data.decode())
            
            self.assertTrue(data['message'] == 'Project already exists!')
            self.assertEqual(res.status_code, 409)