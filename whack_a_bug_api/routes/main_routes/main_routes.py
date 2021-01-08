from flask import jsonify, request, abort, make_response
from flask.views import MethodView
from whack_a_bug_api.models.projects import Project
from whack_a_bug_api.models.bugs import Bug
from . import main
from whack_a_bug_api.db import db

class ProjectsView(MethodView):
    """Class controlling all api routes for projects"""
    
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
        
        if title:
            existing_project = Project.query.filter_by(title = title).first()
            
            if existing_project is None:
                try:
                    project = Project(title = title)
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

#define the API resources
projects_view = ProjectsView.as_view('projects_api')

#add url rules for endpoints
main.add_url_rule(
    '/api/main/projects',
    view_func=projects_view
)

# @main.route('/projects', methods=['GET', 'POST'])
# def getProjects():
#     if request.method == 'POST':
#         title = request.json['title']
        
#         if title:
#             existing_project = Project.query.filter_by(title = title).first()
                        
#             if existing_project is None:
#                 project = Project(title=title)
#                 project.save()
                
#                 res = jsonify({
#                     'id': project.id,
#                     'title': project.title,
#                     'created_on': project.created_on,
#                     'modified_on': project.modified_on 
#                 })
#                 res.status_code = 201
#                 return res
#             else:
#                 data = {'message': 'Project already exists!'}
#                 return make_response(jsonify(data), 409)
#         else:
#             data = {'message': 'Title is required!'}
#             return make_response(jsonify(data), 400)
#     else:
#         projects = Project.get_all()
#         results = []
        
#         for project in projects:
#             obj = {
#                 'id': project.id,
#                 'title': project.title,
#                 'created_on': project.created_on,
#                 'modified_on': project.modified_on
#             }
#             results.append(obj)
        
#         res = jsonify(results)
#         res.status_code = 200
#         return res
    
@main.route('/projects/project/<int:id>', methods=['GET'])
def get_project_by_id(id):
    project = Project.query.filter_by(id = id).first()
    
    if not project:
        abort(404)
        
    res = jsonify({
        'id': project.id,
        'title': project.title,
        'created_on': project.created_on,
        'modified_on': project.modified_on
    })
    res.status_code = 200
    return res


@main.route('/projects/project/<int:id>/update', methods=['PUT'])
def update_project(id):
    project = Project.query.filter_by(id = id).first()
    
    if not project:
        abort(404)
        
    if request.method == 'PUT':
        project.title = request.json['title']
        project.save()
        
        res = jsonify({
            'id': project.id,
            'title': project.title,
            'created_on': project.created_on
        })
        res.status_code = 200
        return res

@main.route('/projects/delete', methods=['DELETE'])
def delete_project():
    if request.method == 'DELETE':
        ids = request.json['selectedIDs']
        data = Project.delete(ids)
    
        return make_response(jsonify(data), 200)
    

@main.route('/bugs', methods=['GET', 'POST'])
def getBugs():
    if request.method == 'POST':
        title = request.form.get('title')
        project = Project.query.filter_by(title = request.form.get('project_name')).first()
        
        if title:
            bug = Bug(
                title = title,
                project_name = project.title,
                project_id = project.id
            )
            
            bug.save()
            
            res = jsonify({
                'id': bug.id,
                'title': bug.title,
                'project_id':bug.project_id,
                'ticket_ref': bug.ticket_ref
            })
            res.status_code = 201
            return res
    else:
        bugs = Bug.get_all()
        results = []
        
        for bug in bugs:
            obj = {
                'id': bug.id,
                'title': bug.title,
                'project_name': bug.project_name,
                'project_id':bug.project_id,
                'ticket_ref': bug.ticket_ref
            }
            results.append(obj)
            
        res = jsonify(results)
        res.status_code = 200
        return res