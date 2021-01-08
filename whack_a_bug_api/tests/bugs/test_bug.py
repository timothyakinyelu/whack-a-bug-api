from flask import json
from whack_a_bug_api.tests.baseCase import BaseCase
from whack_a_bug_api.models.projects import Project
from whack_a_bug_api.models.bugs import Bug

class BugTests(BaseCase):
    def test_bug_issue_can_be_created(self):
        project = Project(title = 'Food Blog')
        project.save()
        
        self.bug = {
            'title': 'Unable to login',
            'project_name': 'Food Blog'
        }
        
        with self.client:
            res = self.client.post('/api/main/bugs', data = json.dumps(self.bug), content_type = 'application/json')
            data = json.loads(res.data.decode())
            
            self.assertEqual(res.status_code, 201)
            self.assertIn('Unable to login', data['data']['title'])
            self.assertIn('WB1001', data['data']['ticket_ref'])
            self.assertTrue(data['message'] == 'Bug Issue created successfully!')
            
            
    def test_all_issues_can_be_fetched(self):
        project = Project(title = 'Food Blog')
        project.save()
        
        self.bug = {
            'title': 'Unable to login',
            'project_name': 'Food Blog'
        }
        
        with self.client:
            res = self.client.post('/api/main/bugs', data = json.dumps(self.bug), content_type = 'application/json')
            self.assertEqual(res.status_code, 201)
            
            resp = self.client.get('/api/main/bugs')
            data = json.loads(resp.data.decode())
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('WB1001', data['data'][0]['ticket_ref'])