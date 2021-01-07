from flask import jsonify, request
from whack_a_bug_api.models.projects import Project
from . import auth


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