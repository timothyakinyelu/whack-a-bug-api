from  whack_a_bug_api.db import db

project_user_table = db.Table('project_user', db.Model.metadata,
    db.Column(
        'project_id',
        db.Integer,
        db.ForeignKey('projects.id')
    ),   
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id')
    )                           
)