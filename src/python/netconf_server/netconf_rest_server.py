###
# ============LICENSE_START=======================================================
# Netconf Server
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

import logging as sys_logging
from flask import Flask, logging, make_response, Response


class NetconfRestServer:
    _rest_server: Flask = Flask("server")
    sys_logging.basicConfig(level=sys_logging.DEBUG)
    logger = logging.create_logger(_rest_server)

    def __init__(self, host='0.0.0.0', port=6555):
        self._host = host
        self._port = port

    def start(self):
        Flask.run(
            NetconfRestServer._rest_server,
            host=self._host,
            port=self._port
        )

    @staticmethod
    @_rest_server.route("/healthcheck")
    def __health_check():
        return "UP"

    @staticmethod
    def __create_http_response(code, message):
        return make_response(
            Response(message, headers={'Content-Type': 'application/json'}),
            code)
