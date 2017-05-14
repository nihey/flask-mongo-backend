class Config(object):
    DEBUG = False

    # We cannot use MONGO_URI yet - reason:
    # https://github.com/dcrosta/flask-pymongo/issues/73
    MONGO_DBNAME = 'project'
    MONGO_CONNECT = False

    DOMAIN = 'https://project.com'
