from whack_a_bug_api.db import db
from flask_sqlalchemy import event


def generate_ticket_ref():
        last_issue = Bug.query.filter().order_by(Bug.id.desc()).first()
        if not last_issue:
            return 'WB1001'
        
        ticket_ref = last_issue.ticket_ref
        ticket_no = int(ticket_ref.split('WB')[-1])
        new_ticket_no = ticket_no + 1
        new_ticket_ref = 'WB' + str(new_ticket_no)
        return new_ticket_ref

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
        default=generate_ticket_ref,
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
    
    
    def save(self):
        """Commit model values to database"""
        
        db.session.add(self)
        db.session.commit()
    
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
                
            
        
    
        
        
    
    