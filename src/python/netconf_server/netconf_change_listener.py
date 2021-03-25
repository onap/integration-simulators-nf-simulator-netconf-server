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

logger = logging.getLogger("netconf_saver")


class NetconfChangeListener(object):

    def __init__(self, subscriptions: list):
        self.subscriptions = subscriptions

    def run(self, session):
        for subscription in self.subscriptions:
            subscription.callback_function = self.__on_module_configuration_change
            subscription.subscribe_on_model_change(session)

    @staticmethod
    def __on_module_configuration_change(config_change_data: ConfigChangeData):
        logger.info("Received module changed: %s , %s " % (config_change_data.event, config_change_data.changes))
