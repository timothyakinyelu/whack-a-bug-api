from whack_a_bug_api.config import *

def loadConfig(MODE):
    """Checks environment variables before loading application"""
    
    try:
        if MODE == 'production':
            return ProductionConfig
        elif MODE == 'testing':
            return TestConfig
        else:
            return DevelopmentConfig
    except ImportError:
        return BaseConfig