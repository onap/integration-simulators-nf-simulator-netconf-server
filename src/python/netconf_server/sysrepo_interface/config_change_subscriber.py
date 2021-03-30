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

import logging

from netconf_server.sysrepo_interface.config_change_data import ConfigChangeData

logger = logging.getLogger("sysrepo_config_change_subscriber")


class ConfigChangeSubscriber(object):

    def __init__(self, module_name: str, callback_function: callable = None):
        self.module_name = module_name
        if callback_function is None:
            self.callback_function = self.default_callback
        else:
            self.callback_function = callback_function

    def subscribe_on_model_change(self, session):
        logger.info("Subscribing on config change for module %s" % self.module_name)
        session.subscribe_module_change(
            self.module_name, None, self.on_module_have_changed, asyncio_register=True
        )

    async def on_module_have_changed(self, event: str, req_id: int, changes: list, private_data: any):
        logger.debug("Module changed: %s (request ID %s)" % (event, req_id))
        self.callback_function(ConfigChangeData(event, req_id, changes))

    @staticmethod
    def default_callback(config_change_data: ConfigChangeData):
        logger.info("Received module changed: %s , %s " % (config_change_data.event, config_change_data.changes))
