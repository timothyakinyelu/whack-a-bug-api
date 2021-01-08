from flask import jsonify, request, abort, make_response
from whack_a_bug_api.models.projects import Project
from whack_a_bug_api.models.bugs import Bug
from . import main
from whack_a_bug_api.db import db


@main.route('/projects', methods=['GET', 'POST'])
def getProjects():
    if request.method == 'POST':
        title = request.json['title']
        
        if title:
            existing_project = Project.query.filter_by(title = title).first()
                        
            if existing_project is None:
                project = Project(title=title)
                project.save()
                
                res = jsonify({
                    'id': project.id,
                    'title': project.title,
                    'created_on': project.created_on,
                    'modified_on': project.modified_on 
                })
                res.status_code = 201
                return res
            else:
                data = {'message': 'Project already exists!'}
                return make_response(jsonify(data), 409)
        else:
            data = {'message': 'Title is required!'}
            return make_response(jsonify(data), 400)
    else:
        projects = Project.get_all()
        results = []
        
        for project in projects:
            obj = {
                'id': project.id,
                'title': project.title,
                'created_on': project.created_on,
                'modified_on': project.modified_on
            }
            results.append(obj)
        
        res = jsonify(results)
        res.status_code = 200
        return res
    
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