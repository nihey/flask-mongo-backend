from project.collections.base import BaseCollection


class User(BaseCollection):
    __collection_keys__ = [
        {'username'},
        {'email'},
    ]
