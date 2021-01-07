from whack_a_bug_api.db import db


class Project(db.Model):
    """ Model representing projects table"""
    
    __tablename__ = 'projects'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True,
    )
    title = db.Column(
        db.String(50),
        unique = True,
        nullable = False
    )
    description = db.Column(
        db.Text
    )
    created_on = db.Column(
        db.DateTime,
        default = db.func.current_timestamp()
    )
    modified_on = db.Column(
        db.DateTime,
        default = db.func.current_timestamp(),
        onupdate = db.func.current_timestamp()
    )
    bugs = db.relationship(
        'Bug',
        backref = 'project',
        lazy = 'joined'
    )
    
    
    @staticmethod
    def get_all():
        return Project.query.all()
    
    
    def __repr__(self):
        return "<Project: {}>".format(self.title)