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
    _http_server: Flask = Flask("server")
    sys_logging.basicConfig(level=sys_logging.DEBUG)
    logger = logging.create_logger(_http_server)

    @staticmethod
    def run_app(name, host='0.0.0.0', port=6555):
        Flask.run(NetconfRestServer._http_server, host=host, port=port)

    @staticmethod
    def _set_up_http_client(import_name):
        NetconfRestServer._http_server.name = import_name

    @staticmethod
    @_http_server.route("/")
    def health_check():
        return "UP"

    @staticmethod
    def create_http_response(code, message):
        return make_response(
            Response(message, headers={'Content-Type': 'application/json'}),
            code)
