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
from netconf_server.netconf_rest_server import NetconfRestServer

from netconf_server.netconf_change_listener import NetconfChangeListener
from netconf_server.netconf_change_listener_factory import NetconfChangeListenerFactory
from netconf_server.sysrepo_configuration.sysrepo_configuration_loader import SysrepoConfigurationLoader, \
    ConfigLoadingException
from netconf_server.sysrepo_interface.sysrepo_client import SysrepoClient

logging.basicConfig(
    handlers=[logging.StreamHandler(), logging.FileHandler("/logs/netconf_server.log")],
    level=logging.DEBUG
)
logger = logging.getLogger("netconf_server")


def run_server_forever(session, change_listener: NetconfChangeListener, server_rest: NetconfRestServer):
    change_listener.run(session)
    server_rest.start()


def create_change_listener() -> NetconfChangeListener:
    configuration = SysrepoConfigurationLoader.load_configuration(sys.argv[1])
    return NetconfChangeListenerFactory(configuration.models_to_subscribe_to).create()


def create_rest_server() -> NetconfRestServer:
    return NetconfRestServer()


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        try:
            netconf_change_listener = create_change_listener()
            rest_server = create_rest_server()
            SysrepoClient().run_in_session(run_server_forever, netconf_change_listener, rest_server)
        except ConfigLoadingException:
            logger.error("File to load configuration from file %s" % sys.argv[1])
    else:
        logger.error("Missing path to file with configuration argument required to start netconf server.")
