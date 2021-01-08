from flask import Flask
from whack_a_bug_api.helpers.load_config import loadConfig
from flask_login import LoginManager

login_manager = LoginManager()

def createApp():
    app = Flask(__name__, instance_relative_config=True)
    mode = app.env
    
    Config = loadConfig(mode)
    app.config.from_object(Config)
    
    from whack_a_bug_api.db import db
    db.init_app(app)
    login_manager.init_app(app)
    
    from whack_a_bug_api.models import bugs, projects
    
    with app.app_context():
        #add route blueprints
        from whack_a_bug_api.routes.main_routes import main_routes
        
        app.register_blueprint(main_routes.main)
        
        db.create_all()
        return app