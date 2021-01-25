from whack_a_bug_api.db import db

class Role(db.Model):
    """ Model representing roles table"""
    
    __tablename__ = 'roles'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    name = db.Column(
        db.String(30),
        nullable = False
    )
    users = db.relationship(
        'User',
        backref = 'role',
        lazy = 'joined'
    )