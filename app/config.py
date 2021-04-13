class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'ERV+t4937-8t4/8s45d7gF'
    SESSION_SECURE = False

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    TESTING = True

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'
    USERNAME = 'Adamacy'
    PASSWORD = 'NieInterere123'
    MONGO_DB = 'PatientCard'
    MONGO_URI = f'mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.umzi0.mongodb.net/{MONGO_DB}?retryWrites=true&w=majority'

class TestingConfig(Config):
    TESTING = True