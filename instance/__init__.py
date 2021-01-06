from flask import flask
from whack_a_bug_api.helpers.load_config import loadConfig
from flask_login import LoginManager

login_manager = LoginManager()

def createApp():
    app = Flask(__name__)
    mode = app.env
    
    Config = loadConfig(mode)
    app.config.from_object(Config)
    
    from instance.db import db
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        #add route blueprints
        
        db.create_all()
        return app