import os
from datetime import datetime
from inspect import isclass

def log(*args):
    string = ' '.join([unicode(a).encode('utf-8') for a in args])
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '-', string


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
