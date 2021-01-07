from whack_a_bug_api.db import db
from flask_sqlalchemy import event
from sqlalchemy.schema import Sequence


class Bug(db.Model):
    """ Model representing bugs table"""
    
    __tablename__ = 'bugs'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    title = db.Column(
        db.String(50),
        nullable = False
    )
    description = db.Column(
        db.Text
    )
    severity = db.Column(
        db.String(30),
        server_default = 'LOW'
    )
    bug_status = db.Column(
        db.String(30),
        server_default = 'NEW'
    )
    bug_track_status = db.Column(
        db.String(30),
        server_default = 'Ongoing'
    )
    ticket_ref = db.Column(
        db.String(50),
        Sequence('bug_ticket_ref_seq', start=1001, increment=1),
        nullable = False
    )
    project_name = db.Column(
        db.String(50),
        nullable = False
    )
    project_id = db.Column(
        db.Integer,
        db.ForeignKey('projects.id')
    )
    created_on = db.Column(
        db.DateTime,
        default = db.func.current_timestamp()
    )
    closed_on = db.Column(
        db.DateTime
    )
    
    
    @staticmethod
    def get_all():
        """ Fetch all Bugs from database"""
        
        return Bug.query.all()
    
    @event.listens_for(db.session, 'before_flush')
    def set_closed_on(*args):
        sess = args[0]
        for obj in sess.new:
            if not isinstance(obj, Bug):
                continue
                
            if obj.bug_track_status == 'Completed':
                if self.bug_track_status == obj.bug_track_status:
                    continue
                    
                self.closed_on = db.func.current_timestamp()
    
    
    def __repr__(self):
        return "<Bug: {}>".format(self.title)
                
            
        
    
        
        
    
    