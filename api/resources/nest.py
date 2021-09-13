from http import HTTPStatus

from flask import jsonify, request
from flask_restful import Resource

from auth.base import auth
from nest import nestify


class Nestify(Resource):
    """
    Nestify REST-API resource

    POST /nestify?=[group_by=<arg_1>,<arg_2>...]

    """

    @auth.login_required
    def post(self):
        status = HTTPStatus.OK
        groups = request.args.get('group_by', [])
        if not request.is_json or not type(request.json) is list:
            return 'Invalid JSON body provided', HTTPStatus.BAD_REQUEST

        if groups:
            groups = [str(item).lower().strip() for item in groups.split(',')]

        try:
            result = nestify(request.json, *groups).as_dict()
            if not result:
                status = HTTPStatus.NO_CONTENT
        except Exception as e:
            result, status = str(e), HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            return jsonify(result).json, status
