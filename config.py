import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # After personalized questions, you get this many books recommended 
    BOOK_MAP_STARTER_CHOICES = 4

    # First book params: after finishing a book it can reveal MIN to MAX branches.
    BOOK_MAP_ROOT_CHILDREN_MIN = 4
    BOOK_MAP_ROOT_CHILDREN_MAX = 6

    # after first book
    BOOK_MAP_FOLLOWUP_CHILDREN_MIN = 1
    BOOK_MAP_FOLLOWUP_CHILDREN_MAX = 4

    # Recommendation tuning param; to adjust using observed results.
    USER_RECOMMENDATION_EXPLORATION_RATE = 0.20
    
    # Default value for classroom assignment pass threshold
    STUDENT_PASS_PERCENT_DEFAULT = 70.0

    # Auto publish difficulties on algorithm finish; by default suggests.
    BOOK_DIFFICULTY_AUTO_PUBLISH = False


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}