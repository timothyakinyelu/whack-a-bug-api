from flask import jsonify, request
from whack_a_bug_api.models.projects import Project
from whack_a_bug_api.models.bugs import Bug
from . import auth
from whack_a_bug_api.db import db


@auth.route('/projects', methods=['GET', 'POST'])
def getProjects():
    if request.method == 'POST':
        title = request.form.get('title')
                    
        if title:
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
    
    
@auth.route('/bugs', methods=['GET', 'POST'])
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
            
            db.session.add(bug)
            db.session.flush()
            db.session.commit()
            
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