import os
import json
from datetime import datetime
from inspect import isclass

from flask import Response, session
from bson.objectid import ObjectId


def log(*args):
    string = ' '.join([unicode(a).encode('utf-8') for a in args])
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '-', string)


def json_response(dict_, code=200):
    return Response(json.dumps(dict_), code, mimetype='application/json')


def unset_user():
    session.pop('user_id', None)


def set_user(user):
    session['user_id'] = unicode(user['_id'])
    return user


def get_user():
    from project.collections.user import User
    return User.find_one({'_id': ObjectId(session.get('user_id'))})


def get_subclasses(directory, cls):
    """Get all the classes within a directory"""
    # TODO: Implement a multilevel search
    modules = [m.replace('.py', '') for m in os.listdir(directory)
               if m.endswith('py')]

    subclasses = []
    base = directory.replace('/', '.')
    for module in modules:
        # Import the module and walk the steps untill the leaf one
        path = (base + '.' + module).replace('.__init__', '')
        module = __import__(path)
        for step in path.split('.')[1:]:
            module = getattr(module, step)

        for variable in module.__dict__.itervalues():
            if isclass(variable) and issubclass(variable, cls):
                subclasses.append(variable)

    for subdir in os.listdir(directory):
        # Avoid infinite loops by removing __init__.py
        if subdir.startswith('__init__'):
            continue

        subdir = os.path.join(directory, subdir)
        if os.path.isdir(subdir):
            subclasses += get_subclasses(subdir, cls)

    return subclasses
