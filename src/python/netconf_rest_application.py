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
import sys
import logging

from netconf_server.netconf_app_configuration import NetconfAppConfiguration
from netconf_server.netconf_rest_server import NetconfRestServer
from netconf_server.sysrepo_configuration.sysrepo_configuration_manager import SysrepoConfigurationManager

from netconf_server.sysrepo_interface.sysrepo_client import SysrepoClient

logging.basicConfig(
    handlers=[logging.StreamHandler(), logging.FileHandler("/logs/netconf_rest_application.log")],
    level=logging.DEBUG
)
logger = logging.getLogger("netconf_rest_application")


def start_rest_server(session, connection, server_rest: NetconfRestServer):
    sysrepo_cfg_manager = create_conf_manager(session, connection)
    server_rest.start(sysrepo_cfg_manager)


def create_rest_server() -> NetconfRestServer:
    return NetconfRestServer()


def create_conf_manager(session, connection) -> SysrepoConfigurationManager:
    return SysrepoConfigurationManager(session, connection)


if __name__ == "__main__":
    app_configuration, error = NetconfAppConfiguration.get_configuration(sys.argv)  # type: NetconfAppConfiguration, str

    if app_configuration:
        logger.info("Netconf rest application configuration: {}".format(app_configuration))
        rest_server = create_rest_server()
        SysrepoClient().run_in_session(start_rest_server, rest_server)
    else:
        logger.error(error)
