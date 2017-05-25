from project.api.base import BaseResource
from project.collections.user import User
from project.utils import get_user, set_user, unset_user, json_response


class LoginResource(BaseResource):
    """Provides logging-in and out utilities"""

    route = '/login'

    def get(self):
        """Check if a user is logged in"""
        user = get_user()
        if not user:
            return json_response({'error': 'not logged in'}, code=401)
        return user

    def post(self):
        """Logs a user in"""
        email = self.get_arg('email')
        password = self.get_arg('password', '')
        user = User.authenticate(email, password)
        if not user:
            return json_response({'error': 'not authenticated'}, code=401)
        return set_user(user)

    def delete(self):
        """Logs a user out"""
        unset_user()
        return {'message': 'OK'}
