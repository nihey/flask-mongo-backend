from flask import request
from flask_restful import Resource

from project.app import app


class BaseResource(Resource):
    """Provides some extra perks into Flask Restful's Resources"""

    # The domain to be allowed on CORS
    domain = app.config['DOMAIN']

    #: The route on which the Resource will be
    #:
    #: Examples:
    #:
    #: route = '/video/<code>'
    #: route = '/video'
    route = None

    def get_arg(self, attr, default=None):
        """Return the argument, wheter it came from querystring or form data"""
        return request.form.get(attr, request.args.get(attr, default))

    def options(self, *args, **kwargs):
        """Just in case a Browser wants to do a CORS check"""
        return {'message': 'OK'}


class GeneralResource(BaseResource):
    """General Resources CRUD operations"""
    route = '/<resource>'

    def get(self):
        """TBD"""
        pass

    def post(self):
        """TBD"""
        pass

    def put(self):
        """TBD"""
        pass

    def delete(self):
        """TBD"""
        pass
