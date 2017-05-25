class Config(object):
    DEBUG = False

    # We cannot use MONGO_URI yet - reason:
    # https://github.com/dcrosta/flask-pymongo/issues/73
    MONGO_DBNAME = 'project'
    MONGO_CONNECT = False

    DOMAIN = 'https://project.com'

    SECRET_KEY = 'bc48531e23fff4ca67ec7edeafacaef1bc534fa867979c15daf7495aa5b9b4a738142eec76932330aed7a3f76453de0f'
