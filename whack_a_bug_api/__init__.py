from flask import Flask
from whack_a_bug_api.helpers.load_config import loadConfig
from flask_login import LoginManager
from flask_migrate import Migrate

login_manager = LoginManager()
migrate = Migrate()

def createApp():
    app = Flask(__name__, instance_relative_config=True)
    mode = app.env
    
    Config = loadConfig(mode)
    app.config.from_object(Config)
    
    from whack_a_bug_api.db import db
    from whack_a_bug_api.models import bugs, projects, users, pivots
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    with app.app_context():
        #add route blueprints
        from whack_a_bug_api.routes.main_routes import main_routes
        from whack_a_bug_api.routes.auth_routes import auth_routes
        
        app.register_blueprint(main_routes.main)
        app.register_blueprint(auth_routes.auth)
        
        return app