# ================================================================================
# Copyright (C) 2021 Nokia. All rights reserved.
# ================================================================================
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============LICENSE_END=========================================================
###
import json
import logging


class SysrepoConfigurationManager(object):
    logger = logging.getLogger(__name__)

    def __init__(self, session, connection):
        self._connection = connection
        self._session = session

    def __parse_config_data(self, config_data):
        self.logger.debug(config_data)
        ctx = self._connection.get_ly_ctx()
        data = ctx.parse_data_mem(
            config_data,
            "xml",
            config=True,
            strict=False,
        )
        return data

    def change_configuration(self, config_data: str, module_name: str):
        data = self.__parse_config_data(config_data)
        self._session.replace_config_ly(data, module_name)

    def get_configuration(self, module_name: str):
        data = self._session.get_data("/" + module_name + ":*")
        return json.dumps(data, indent=4)
