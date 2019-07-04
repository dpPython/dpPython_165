from abc import ABC, abstractmethod

from flask import jsonify
from json import loads
from requests import get, put, post

LOGGED_IN = 'logged in'


class BasicSender(ABC):
    basic_url = ""

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def post(self, *args, **kwargs):
        pass

    @abstractmethod
    def put(self, *args, **kwargs):
        pass


class SessionService(BasicSender):
    basic_url = 'http://authentication_service:6000/sessions/{uuid}'.format(
        uuid='')

    def get(self, auth_session_uuid):
        session = get(self.basic_url.format(uuid=auth_session_uuid))
        json_response = loads(session.text)
        if json_response.get('status') == LOGGED_IN:
            json_response.status_code = 200
        else:
            json_response.status_code = 300
        return json_response

    def post(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass


class ProjectService(BasicSender):
    basic_url = "http://projects_service:5000/api/projects/{uuid}".format(
        uuid='')

    def post(self, project_service_uuid, data):
        data_chunk = jsonify(data)
        return post(self.basic_url.format(uuid=project_service_uuid),
                    {'data': data_chunk})

    def put(self, project_service_uuid, status):
        return put(self.basic_url.format(uuid=project_service_uuid),
                   {'status': status})

    def get(self, *args, **kwargs):
        pass
