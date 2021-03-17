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
import os
from configparser import ConfigParser

from netconf_server.sysrepo_configuration.sysrepo_configuration import SysrepoConfiguration

MODELS_LIST_TAG = "models"
SUBSCRIPTION_TAG = "SUBSCRIPTION"

logger = logging.getLogger("sysrep_configuration_loader")


class SysrepoConfigurationLoader(object):

    # configuration_file must be in .ini format
    @staticmethod
    def load_configuration(configuration_file: str) -> SysrepoConfiguration:
        if os.path.isfile(configuration_file):
            config_object = ConfigParser()
            config_object.read(configuration_file)
            if SUBSCRIPTION_TAG in config_object and MODELS_LIST_TAG in config_object[SUBSCRIPTION_TAG]:
                logger.info("Loading configuration from file %s" % configuration_file)
                models_to_subscribe_to = config_object[SUBSCRIPTION_TAG][MODELS_LIST_TAG].split(",")
                return SysrepoConfiguration(models_to_subscribe_to)
            else:
                logger.warning("Loading configuration failed, %s is not valid configuration file" % configuration_file)
                raise ConfigLoadingException(
                    "Loading sysrepo configuration have failed, %s is not correct config file" % configuration_file
                )
        else:
            logger.warning("Loading configuration failed, %s does not exist or is not a file" % configuration_file)
            raise ConfigLoadingException(
                "Loading sysrepo configuration have failed, %s is not valid file" % configuration_file
            )


class ConfigLoadingException(Exception):
    pass
