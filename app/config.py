class Config(object):
    """ Configs for user"""

    ENV = 'development'
    FLASK_ENV = 'development'
    TESTING = False
    DEBUG = False
    MONGO_USERNAME = 'Adamacy'
    MONGO_PASSWORD = 'NieInterere123'
    MONGO_URI = f'mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.umzi0.mongodb.net/PatientCard?retryWrites=true&w=majority'
    SECRET_KEY = '/8awr9744weasd464934/*6rg*'
    MONGO_DATABASE = 'PatientCard'
    SESSION_TYPE = 'mongodb'
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    
    DEBUG = True
    TESTING = False
    
class TestingConfig(Config):
    TESTING = True