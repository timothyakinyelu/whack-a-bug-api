from flask import jsonify
from whack_a_bug_api.models.projects import Project
from . import auth


@auth.route('/')
def getProjects():
    return Project.get_all()