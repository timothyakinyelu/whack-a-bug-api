from flask import Flask, request, current_app
from whack_a_bug_api.helpers.load_config import loadConfig
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import event
import jwt

login_manager = LoginManager()
migrate = Migrate()

def createApp():
    app = Flask(__name__, instance_relative_config=True)
    mode = app.env
    
    Config = loadConfig(mode)
    app.config.from_object(Config)
    
    from whack_a_bug_api.db import db
    from whack_a_bug_api.models import bugs, projects, users, pivots, roles
    
    @event.listens_for(roles.Role.__table__, 'after_create')
    def insert_initial_values(*args, **kwargs):
        db.session.add(Role(name = 'developer'))
        db.session.add(Role(name = 'tester'))
        db.session.add(Role(name = 'lead'))
        db.session.commit()
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    @login_manager.request_loader
    def load_user_from_request(request):
        auth_headers = request.headers.get('Authorization', '').split()
        
        if len(auth_headers) != 2:
            return None
        
        try:
            token = auth_headers[1]
    
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'], options={"require": ["exp"]})
            User = users.User
            user = User.query.filter_by(public_id = data['sub']).first()
            
            if not user:
                return 'User not found!'
            return user
        except jwt.ExpiredSignatureError:
            return 'Token Signature has expired, please log in again.'
        except jwt.InvalidSignatureError:
            return 'Invalid token, please log in again.'
            
    
    with app.app_context():
        #add route blueprints
        from whack_a_bug_api.routes.main_routes import main_routes
        from whack_a_bug_api.routes.auth_routes import auth_routes
        
        app.register_blueprint(main_routes.main)
        app.register_blueprint(auth_routes.auth)
        
        return app