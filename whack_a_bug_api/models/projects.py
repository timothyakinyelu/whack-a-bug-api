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
    
    def save(self):
        """Commit model values to database"""
        
        db.session.add(self)
        db.session.commit()
        
    def delete(ids):
        """Delete selected projects from database"""
        
        db.session.query(Project).filter(Project.id.in_(ids)).delete(synchronize_session = False)
        db.session.commit()
        
        data = {'message': 'Project(s) deleted Successfully!'}
        return data
    
    @staticmethod
    def get_all():
        """ Fetch all Bugs from database"""
        
        return Project.query.all()
    
    
    def __repr__(self):
        return "<Project: {}>".format(self.title)