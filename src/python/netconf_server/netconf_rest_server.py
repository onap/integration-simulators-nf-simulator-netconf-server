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

from flask import Flask, logging, make_response, Response, request, jsonify

from netconf_server.netconf_kafka_client import NetconfKafkaClient
from netconf_server.sysrepo_configuration.sysrepo_configuration_manager import SysrepoConfigurationManager


class NetconfRestServer:
    _rest_server: Flask = Flask("server")
    logger = logging.create_logger(_rest_server)
    _configuration_manager: SysrepoConfigurationManager
    _kafka_topic: str
    _kafka_client: NetconfKafkaClient

    def __init__(self, host='0.0.0.0', port=6555):
        self._host = host
        self._port = port

    def start(self,
              configuration_manager: SysrepoConfigurationManager,
              kafka_client: NetconfKafkaClient,
              kafka_topic: str):
        NetconfRestServer._configuration_manager = configuration_manager
        NetconfRestServer._kafka_client = kafka_client
        NetconfRestServer._kafka_topic = kafka_topic
        Flask.run(
            NetconfRestServer._rest_server,
            host=self._host,
            port=self._port
        )

    @staticmethod
    @_rest_server.route("/healthcheck")
    def _health_check():
        return "UP"

    @staticmethod
    @_rest_server.route("/readiness")
    def _readiness_check():
        if NetconfRestServer._kafka_client:
            return Response('Ready', status=200)
        else:
            return Response('Not Ready', status=503)

    @staticmethod
    @_rest_server.route("/change_config/<path:module_name>", methods=['POST'])
    def _change_config(module_name):
        config_data = request.data.decode("utf-8")
        NetconfRestServer._configuration_manager.change_configuration(config_data, module_name)
        return NetconfRestServer.__create_http_response(202, "Accepted")

    @staticmethod
    @_rest_server.route("/change_history")
    def _change_history():
        history = NetconfRestServer._kafka_client.get_all_messages_from(NetconfRestServer._kafka_topic)
        return jsonify(history), 200

    @staticmethod
    @_rest_server.route("/get_config/<path:module_name>", methods=['GET'])
    def _get_config(module_name):
        data = NetconfRestServer._configuration_manager.get_configuration(module_name)
        return NetconfRestServer.__create_http_response(200, data)

    @staticmethod
    def __create_http_response(code, message):
        return make_response(
            Response(message, headers={'Content-Type': 'application/json'}),
            code)
