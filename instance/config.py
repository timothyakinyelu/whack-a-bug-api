import os

class BaseConfig:
    """ Default app configuration"""
    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    CSRF_ENABLED = True
    
    
class DevelopmentConfig(BaseConfig):
    """App configuration in development mode"""
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
class ProductionConfig(BaseConfig):
    """App configuration in production mode"""
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    TESTING = False
    
class TestConfig(BaseConfig):
    """App cofiguration in test mode"""
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE')
    TESTING = True
    DEBUG = True
    HASH_ROUNDS = 1
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    
app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig
}