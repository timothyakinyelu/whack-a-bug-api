from flask import jsonify, request, abort, make_response
from flask.views import MethodView
from whack_a_bug_api.models.projects import Project
from whack_a_bug_api.models.users import User
from whack_a_bug_api.models.bugs import Bug
from . import main
from whack_a_bug_api.db import db
from flask_login import login_required

class ProjectsView(MethodView):
    """Class controlling all api routes for projects"""
    
    decorators = [login_required]
    
    def get(self):
        projects = Project.get_all()
        results = []
        
        for project in projects:
            obj = {}
            
            obj['id'] = project.id
            obj['title'] = project.title
            obj['created_on'] = project.created_on
            obj['modified_on'] = project.modified_on
            
            results.append(obj)
        
        res = {'data': results}
        return make_response(jsonify(res), 200)
    
    def post(self):
        form_data = request.get_json()
        title = form_data.get('title')
        ids = form_data.get('users')
        
        if title:
            existing_project = Project.query.filter_by(title = title).first()
            
            if existing_project is None:
                try:
                    project = Project(title = title)
                    if ids is not None:
                        users = User.query.filter(User.id.in_(ids)).all()
                        project.users.extend(users)
                    project.save()
                    
                    data = {}
                    data['id'] = project.id
                    data['title'] = project.title
                    data['created_on'] = project.created_on
                    data['modified_on'] = project.modified_on
                    
                    res = {
                        'data': data,
                        'status': 'success',
                        'message': 'Project created successfully!',
                    }

                    return make_response(jsonify(res), 201)
                except Exception as e:
                    res = {'message': str(e)}
                    return make_response(jsonify(res), 401)
            else:
                data = {'message': 'Project already exists!'}
                return make_response(jsonify(data), 409)
        else:
            data = {'message': 'Title is required!'}
            return make_response(jsonify(data), 400)
        
    def delete(self):
        ids = request.json['selectedIDs']
        data = Project.delete(ids)
        
        return make_response(jsonify(data), 202)

class SingleProjectView(MethodView):
    """Class controlling routes for editing and updating projects"""
    
    decorators = [login_required]
    
    def get(self, id):
        project = Project.query.filter_by(id = id).first()
        
        if project is None:
            abort(404)
            
        data = {}
        data['id'] = project.id
        data['title'] = project.title
        data['description'] = project.description
        data['created_on'] = project.created_on
        
        res = {
            'data': data
        }
        return make_response(jsonify(res), 200)
    
    def put(self, id):
        form_data = request.get_json()
        project = Project.query.filter_by(id = id).first()
        
        if project is None:
            abort(404)
            
        try:
            project.title = form_data.get('title')
            project.description = form_data.get('description')
            project.save()
            
            data = {}
            data['id'] = project.id
            data['title'] = project.title
            data['created_on'] = project.created_on
            
            res = {
                'data': data,
                'status': 'success',
                'message': 'Project updated successfully!'
            }
            
            return make_response(jsonify(res), 200)
        except Exception as e:
            res = {'message': str(e)}
            return make_response(jsonify(res), 401)
     

class BugsView(MethodView):
    """Class controlling all api routes for bugs"""
    
    decorators = [login_required]
    
    def get(self):
        bugs = Bug.get_all()
        results = []
        
        for bug in bugs:
            obj = {}
            
            obj['id'] = bug.id
            obj['title'] = bug.title
            obj['project_name'] = bug.project_name
            obj['project_id'] = bug.project_id
            obj['ticket_ref'] = bug.ticket_ref
            
            results.append(obj)
            
        res = {'data': results}
        return make_response(jsonify(res), 200)
    
    def post(self):
        form_data = request.get_json()
        title = form_data.get('title')
        projectName = form_data.get('project_name')
        
        if title:
            try:
                project = Project.query.filter_by(title = projectName).first()
                
                bug = Bug(
                    title = title,
                    project_name = project.title,
                    project_id = project.id
                )
                bug.save()
                
                data = {}
                data['id'] = bug.id
                data['title'] = bug.title
                data['project_id'] = bug.project_id
                data['ticket_ref'] = bug.ticket_ref
                
                res = {
                    'data': data,
                    'status': 'success',
                    'message': 'Bug Issue created successfully!'
                }
                return make_response(jsonify(res), 201)
            except Exception as e:
                res = {
                    'status': 'failed',
                    'message': str(e)
                }
                return make_response(jsonify(res), 401)
            
class SingleBugView(MethodView):
    """Class controlling routes for editing and updating bug issues"""
    
    decorators = [login_required]
    
    def get(self, id):
        bug = Bug.query.filter_by(id = id).first()
        
        if bug is None:
            abort(404)
            
        data = {}
        data['id'] = bug.id
        data['title'] = bug.title
        data['project_id'] = bug.project_id
        data['ticket_ref'] = bug.ticket_ref
        data['assigned_to'] = bug.assigned_to
        data['bug_status'] = bug.bug_status
        data['test_status'] = bug.test_status
        
        res = {'data': data}
        return make_response(jsonify(res), 200)
    
    def put(self, id):
        form_data = request.get_json()
        userID = form_data.get('userID')
        projectID = form_data.get('projectID')
        bugStatus = form_data.get('bugStatus')
        testStatus = form_data.get('testStatus')
        
        bug = Bug.query.filter_by(id = id).first()
        
        if bug is None:
            abort(404)
        else:    
            if bug.project_id == projectID:
                bug.bug_status = bugStatus
                bug.test_status = testStatus
                
                if userID:
                    link = db.session.query(Project).filter_by(id = projectID) \
                        .filter(Project.users.any(User.id == userID)).first()
                        
                    list_of_users = [obj.id for obj in link.users]
                    
                    if userID in list_of_users:
                        bug.assigned_to = userID
                
                bug.save()
                
                res = {'message': 'Bug issue updated successfully!'}
                return make_response(jsonify(res), 200)
            
        
#define the API resources
projects_view = ProjectsView.as_view('projects_api')
single_project_view = SingleProjectView.as_view('single_project_view')
bugs_view = BugsView.as_view('bugs_api')
single_bug_view = SingleBugView.as_view('single_bug_view')

#add url rules for endpoints
main.add_url_rule(
    '/api/main/projects',
    view_func=projects_view
)
main.add_url_rule(
    '/api/main/projects/project/<int:id>',
    view_func=single_project_view
)
main.add_url_rule(
    '/api/main/bugs',
    view_func=bugs_view
)
main.add_url_rule(
    '/api/main/bugs/<int:id>',
    view_func=single_bug_view
)