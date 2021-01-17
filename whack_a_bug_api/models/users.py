from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from whack_a_bug_api.db import db
from sqlalchemy.orm import validates
from flask_login import UserMixin
from datetime import datetime, timedelta
import re
import jwt
import uuid

class User(db.Model, UserMixin):
    """ Model representing users table"""
    
    __tablename__ = 'users'
    
    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )
    public_id = db.Column(
        db.String(50),
        unique = True
    )
    first_name = db.Column(
        db.String(50),
        nullable = False
    )
    last_name = db.Column(
        db.String(50),
        nullable = False
    )
    username = db.Column(
        db.String(50),
        unique = True,
        nullable = False
    )
    email = db.Column(
        db.String(255),
        nullable = False,
        unique = True
    )
    password = db.Column(
        db.String(50),
        nullable = False
    )
    is_admin = db.Column(
        db.Boolean,
        server_default = "0"
    )
    assigned_issues = db.relationship(
        'Bug',
        backref = 'user',
        lazy = 'joined'
    )
    projects = db.relationship(
        'Project',
        backref = 'user',
        lazy = 'joined'
    )
    
    
    def __init__(self, *args, **kwargs):
        if not 'username' in kwargs:
            self.username = kwargs['last_name'].lower() + kwargs['first_name'].lower()
        
        if not 'public_id' in kwargs:
            self.public_id = str(uuid.uuid4())
            
        super().__init__(*args, **kwargs)

    
    @validates('email')
    def validate_email(self, key, email):
        """Validate email input"""
        
        if not email:
            raise AssertionError('Must provide an email')
        
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError('Provided entry is not an email address')
        
        return email
    
    @validates('username')
    def validate_username(self, key, username):
        """Validate username input"""
        
        if not username:
            raise AssertionError('You must provide a username!')
        
        if User.query.filter(User.username == username).first():
            raise AssertionError('This username already exists!')
        
        if len(username) < 5 and len(username) > 20:
            raise AssertionError('Username must be between 5 and 20 characters long!')
        
        return username
    
    def set_password(self, password):
        """Hash user provided password"""
        
        if not password:
            raise AssertionError('You must enter a password!')
        
        if not re.match("\d.*[A-Z]|[A-Z].*\d", password):
            raise AssertionError('Password must contain 1 capital letter and 1 number!')
        
        if len(password) < 6 and len(password) > 20:
            raise AssertionError('Password must be between 6 and 20 characters long!')
        
        rounds = current_app.config.get('HASH_ROUNDS', 100000)
        self.password = generate_password_hash(password, method='pbkdf2:sha256:{}'.format(rounds))
        
    def check_password(self, password):
        """check if password hash is equivalent to database entry"""
        
        return check_password_hash(self.password, password)
    
    def generate_token(self, public_id):
        """Generates the access token"""
        
        try:
            #create payload
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=2),
                'iat': datetime.utcnow,
                'sub': public_id
            }
            #creat token using payload and secret key
            access_token = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            
            return access_token
        except Exception as e:
            return str(e)
        
    @staticmethod
    def decode_token(token):
        """Decode access_token included in requests"""
        
        