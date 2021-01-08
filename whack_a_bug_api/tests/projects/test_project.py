from whack_a_bug_api.tests.baseCase import BaseCase


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