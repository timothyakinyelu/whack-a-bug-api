from flask import json
from whack_a_bug_api.tests.baseCase import BaseCase
from whack_a_bug_api.models.projects import Project


class ProjectTests(BaseCase):
    def test_projects_can_be_created(self):
        self.project = {'title': 'Food Blog Design'}
        
        with self.client:
            res = self.client.post('/projects', data = self.project)
            self.assertEqual(res.status_code, 201)
            self.assertIn('Food Blog', str(res.data))
            
    def test_api_gets_all_projects(self):
        self.project = {'title': 'Food Blog Design'}
        
        with self.client:
            res = self.client.post('/projects', data = self.project)
            self.assertEqual(res.status_code, 201)
            
            res = self.client.get('/projects')
            self.assertEqual(res.status_code, 200)
            self.assertIn('Food Blog', str(res.data))
            
            
    def test_project_can_be_updated(self):
        existing_project1 = Project(title = 'Food Blog Design')
        existing_project2 = Project(title = 'Ticketing System')
        existing_project1.save()
        existing_project2.save()
        
        self.project = {'title': 'Fashion Blog Design'}
        
        
        with self.client:
            res = self.client.put('/projects/project/1/update', data = json.dumps(self.project), content_type = 'application/json')
            self.assertEqual(res.status_code, 200)
            self.assertIn('Fashion', str(res.data))
    
    
    def test_api_can_get_project_by_id(self):
        existing_project1 = Project(title = 'Food Blog Design')
        existing_project2 = Project(title = 'Ticketing System')
        existing_project1.save()
        existing_project2.save()
        
        with self.client:
            res = self.client.get('/projects/project/2')
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
            res = self.client.delete('/projects/delete', data = json.dumps(dict(selectedIDs = [2])), content_type = 'application/json')
            
            self.assertEqual(res.status_code, 200)
            self.assertIn('Project(s) deleted', str(res.data))
            
            #check if project still exists
            resp = self.client.get('/projects/project/2')
            self.assertEqual(resp.status_code, 404)