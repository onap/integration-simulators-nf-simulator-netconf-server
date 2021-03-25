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
import asyncio
import sys
import logging
from netconf_server.netconf_rest_server import NetconfRestServer

from netconf_server.netconf_change_server import NetconfServer
from netconf_server.netconf_server_factory import NetconfServerFactory
from netconf_server.sysrepo_configuration.sysrepo_configuration_loader import SysrepoConfigurationLoader, \
    ConfigLoadingException
from netconf_server.sysrepo_interface.sysrepo_client import SysrepoClient

logging.basicConfig(
    handlers=[logging.StreamHandler(), logging.FileHandler("/logs/netconf_saver.log")],
    level=logging.DEBUG
)
logger = logging.getLogger("netconf_saver")


def run_server_forever(session, server: NetconfServer, server_rest: NetconfRestServer):
    server.run(session)
    server_rest.run_app("server")


def create_configured_server() -> NetconfServer:
    configuration = SysrepoConfigurationLoader.load_configuration(sys.argv[1])
    return NetconfServerFactory(configuration.models_to_subscribe_to).create()


def create_rest_server() -> NetconfRestServer:
    return NetconfRestServer


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        try:
            netconf_server = create_configured_server()
            rest_server = create_rest_server()
            SysrepoClient().run_in_session(run_server_forever, netconf_server, rest_server)
        except ConfigLoadingException:
            logger.error("File to load configuration from file %s" % sys.argv[1])
    else:
        logger.error("Missing path to file with configuration argument required to start netconf server.")
