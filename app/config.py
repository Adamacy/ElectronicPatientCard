class Config(object):

    DEBUG = False
    TESTING = False
    SECRET_KEY = 'ERV+T4937-8t4/8s45d7gF'
    DATABSE_NAME = 'PatientCard'
    SESSION_SECURE = False

class ProductionConfig(Config):
    TESTING = True

class DevelopmentConfig(Config):
    DEBUG = True

    USERNAME = 'production'
    PASSWORD = '1P8weTwusxac8g0f'
    MONGO_URI = f'mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.umzi0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

class TestingConfig(Config):
    TESTING = True