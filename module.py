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

""" Module """

# import sqlalchemy  # pylint: disable=E0401
from pymongo.errors import CollectionInvalid
from pylon.core.tools import log  # pylint: disable=E0401
from pylon.core.tools import module  # pylint: disable=E0401
from pylon.core.tools.context import Context as Holder  # pylint: disable=E0401

from tools import theme  # pylint: disable=E0401
# from tools import mongo


class Module(module.ModuleModel):
    """ Pylon module """

    def __init__(self, context, descriptor):
        self.context = context
        self.descriptor = descriptor

    def init(self):
        """ Init module """
        log.info("Initializing module")
        # Theme registration
        theme.register_subsection(
            "orch_tool",
            "table", "Issues",
            title="Issues",
            kind="slot",
            permissions={
                "permissions": ["orchestration.issues"],
                "recommended_roles": {
                    "administration": {"admin": True, "viewer": True, "editor": True},
                    "default": {"admin": True, "viewer": True, "editor": True},
                    "developer": {"admin": True, "viewer": True, "editor": True},
                }},
            prefix="issues_table_slot_",
            icon_class="fas fa-server fa-fw",
            # permissions=["orchestration_engineer"],
        )
        #
        # theme.register_page(
        #     "demo", "subdemo", "view",
        #     title="Demo View",
        #     kind="slot",
        #     prefix="demo_slot_view_",
        # )
        # Init services
        self.descriptor.init_all()
        

    def deinit(self):  # pylint: disable=R0201
        """ De-init module """
        log.info("De-initializing module")
        # De-init services
        # self.descriptor.deinit_all()
