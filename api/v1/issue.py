#!/usr/bin/python3
# coding=utf-8

#   Copyright 2022 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" API """
import flask
import flask_restful  # pylint: disable=E0401

from pylon.core.tools import log  # pylint: disable=E0611,E0401

from tools import auth  # pylint: disable=E0401


class API(flask_restful.Resource):  # pylint: disable=R0903
    """ API Resource """

    url_params = ['<int:project_id>/<string:hash_id>']

    def __init__(self, module):
        self.module = module

    @auth.decorators.check_api(["orchestration.issues.issues.view"])
    def get(self, project_id, hash_id):
        result = self.module.get_issue(project_id, hash_id)
        if not result['ok']:
            return result, 400
        result['item']['id'] = str(result['item']['id'])
        return result, 200

    @auth.decorators.check_api({
        "permissions": ["orchestration.issues.issues.edit"],
        "recommended_roles": {
            "administration": {"admin": True, "viewer": False, "editor": True},
            "default": {"admin": True, "viewer": False, "editor": True},
            "developer": {"admin": True, "viewer": False, "editor": True},
        }})
    def put(self, project_id, hash_id):
        payload = flask.request.json
        data = self.module.update_issue(project_id, hash_id, payload)
        return data, 200
    
    @auth.decorators.check_api({
        "permissions": ["orchestration.issues.issues.delete"],
        "recommended_roles": {
            "administration": {"admin": True, "viewer": False, "editor": False},
            "default": {"admin": True, "viewer": False, "editor": False},
            "developer": {"admin": True, "viewer": False, "editor": False},
        }})
    def delete(self, project_id, hash_id):
        result = self.module.delete_issue(project_id, hash_id)
        status_code = 200 if result['ok'] else 400
        return result, status_code

