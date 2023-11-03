from functools import wraps
import os

from flask import abort, request


def auth_decorator(func):
    @wraps(func)
    def auth_request(*args, **kwargs):

        auth = request.headers.get('x-api-key')
        api_key = os.environ.get('API_KEY')

        if auth != api_key:
            abort(401)
        return func(*args, **kwargs)
    return auth_request
