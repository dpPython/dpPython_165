import requests
from flask import abort
from werkzeug.wrappers import Request

LOGGED_IN = 'logged in'


class LoginRequiredMiddleware:

    def __init__(self, wsgi_app, app):
        self.app = wsgi_app
        self.auth_url = app.config.get("FLAKS_AUTH_SERVICE_URL")

    def __call__(self, environ, start_response):
        request = Request(environ)
        if not self._check_auth(request):
            abort(300, 'Access denied')
        return self.app(environ, start_response)

    def _check_auth(self, request):
        auth = request.headers.get('Authorization')
        auth_type, credentials = auth.split(' ')
        if auth_type == 'Bearer':
            session = requests.get(self.auth_url.format(
                uuid=credentials))
            json_response = session.json()
            if json_response.get('status') == LOGGED_IN:
                return True
            return False
