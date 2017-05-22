import re

import pymongo

from project.app import mongo


class BaseCollection(object):

    #: Sets __collection__ property in a dynamic way
    class __metaclass__(type):
        #: The name of the collection (like the name of the table)
        @property
        def __collection__(cls):
            func = lambda x: '-' + x.group(0).lower()
            return re.sub(r'[A-Z]', func, cls.__name__)[1:]

    #: An array of sets, each set defining a unique key of the collection.
    #: The first set of keys is considered to be the primary key
    #:
    #: Example: __collection_keys__ = [{'email'}, {'username'}]
    __collection_keys__ = []

    #
    # DDL-Like Methods
    #

    @classmethod
    def generate_indexes(cls):
        for keys in cls.__collection_keys__:
            uniques = [(k, pymongo.DESCENDING) for k in keys]
            return cls.create_index(uniques, unique=True)

    #
    # MongoDB Methods
    #

    @classmethod
    def create_index(cls, *args, **kwargs):
        return mongo.db[cls.__collection__].create_index(*args, **kwargs)

    @classmethod
    def insert(cls, *args, **kwargs):
        return mongo.db[cls.__collection__].insert(*args, **kwargs)

    @classmethod
    def insert_many(cls, *args, **kwargs):
        return mongo.db[cls.__collection__].insert_many(*args, **kwargs)

    @classmethod
    def find(cls, *args, **kwargs):
        return mongo.db[cls.__collection__].find(*args, **kwargs)

    @classmethod
    def find_one(cls, *args, **kwargs):
        return mongo.db[cls.__collection__].find_one(*args, **kwargs)

    @classmethod
    def update(cls, *args, **kwargs):
        return mongo.db[cls.__collection__].update(*args, **kwargs)

    @classmethod
    def get_or_create(cls, **attrs):
        # Will cause a KeyError if a key is missing
        keys = {key: attrs[key] for key in cls.__collection_keys__[0]}

        # Check if none of the keys is None
        if not all(keys.itervalues()):
            key_names = ' and '.join(keys.iterkeys())
            raise ValueError('{} must not be Falsy'.format(key_names))

        found = cls.find_one(keys)
        if not found:
            cls.insert(attrs)
            return cls.find_one(keys)
        cls.update(keys, {
            '$set': attrs,
        })
        return cls.find_one(keys)
