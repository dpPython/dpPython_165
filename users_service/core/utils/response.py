from flask import Response, jsonify


class MyResponse(Response):
    @classmethod
    def force_type(cls, rspon, environ=None):
        if isinstance(rspon, dict):
            rspon = jsonify(rspon)
        return super(MyResponse, cls).force_type(rspon, environ)
