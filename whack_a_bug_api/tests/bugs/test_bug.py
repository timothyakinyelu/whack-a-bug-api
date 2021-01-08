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
            res = self.client.post('/bugs', data = self.bug)
            self.assertEqual(res.status_code, 201)
            self.assertIn('Unable to login', str(res.data))
            self.assertIn('WB1001', str(res.data))
            
            
    def test_all_issues_can_be_fetched(self):
        project = Project(title = 'Food Blog')
        project.save()
        
        self.bug = {
            'title': 'Unable to login',
            'project_name': 'Food Blog'
        }
        
        with self.client:
            res = self.client.post('/bugs', data = self.bug)
            self.assertEqual(res.status_code, 201)
            self.assertIn('Unable to login', str(res.data))
            self.assertIn('WB1001', str(res.data))
            
            res = self.client.get('/bugs')
            self.assertEqual(res.status_code, 200)
            self.assertIn('WB1001', str(res.data))