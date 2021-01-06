from instance.config import app_config, BaseConfig

def loadConfig(MODE):
    """Checks environment variables before loading application"""
    
    try:
        if MODE == 'production':
            return app_config[MODE]
        elif MODE == 'testing':
            return app_config[MODE]
        else:
            return app_config[MODE]
    except ImportError:
        return BaseConfig