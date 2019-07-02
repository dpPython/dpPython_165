from abc import ABC, abstractmethod

from flask import jsonify
from requests import get, put, post


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
    basic_url = 'http://authentication_service/sessions/{uuid}'.format(uuid='')

    def get(self, auth_session_uuid):
        session = get(self.basic_url.format(uuid=auth_session_uuid))
        return session

    def post(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass


class ProjectService(BasicSender):
    basic_url = "http://projects_service/api/projects/{uuid}".format(uuid='')

    def post(self, project_service_uuid, data):
        data_chunk = jsonify(data)
        return post(self.basic_url.format(uuid=project_service_uuid),
                    {'data': data_chunk})

    def put(self, project_service_uuid, status):
        return put(self.basic_url.format(uuid=project_service_uuid),
                   {'status': status})

    def get(self, *args, **kwargs):
        pass
