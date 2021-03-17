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
import unittest
import os

from netconf_server.sysrepo_configuration.sysrepo_configuration_loader import \
    SysrepoConfigurationLoader, ConfigLoadingException

test_config_file_name = "./test-subscription-configuration.ini"
test_config_file_content = '[SUBSCRIPTION]\nmodels = test-module,test-module-2\n'

test_wrong_config_file_name = "./test-subscription-wrong-configuration.ini"
test_wrong_config_file_content = '[SUBSCRIPTION]\n'

test_non_existing_config_file_name = "./test-subscription-non-existing-configuration.ini"


class TestSysrepoConfigurationLoader(unittest.TestCase):

    def test_should_load_configuration_from_file(self):
        # when
        config = SysrepoConfigurationLoader.load_configuration(test_config_file_name)

        # then
        self.assertEqual(config.models_to_subscribe_to, ["test-module", "test-module-2"])

    def test_should_raise_exception_if_given_configuration_file_is_wrong(self):
        # then
        with self.assertRaises(ConfigLoadingException):
            # when
            SysrepoConfigurationLoader.load_configuration(test_wrong_config_file_name)

    def test_should_raise_exception_if_given_configuration_file_does_not_exist(self):
        # then
        with self.assertRaises(ConfigLoadingException):
            # when
            SysrepoConfigurationLoader.load_configuration(test_non_existing_config_file_name)

    @classmethod
    def setUpClass(cls):
        cls.__create_configuration_file()
        cls.__create_wrong_configuration_file()

    @classmethod
    def tearDownClass(cls):
        cls.__remove_configuration_files()
        cls.__remove_wrong_configuration_files()

    @staticmethod
    def __create_configuration_file():
        f = open(test_config_file_name, "a")
        f.write(test_config_file_content)
        f.close()

    @staticmethod
    def __remove_configuration_files():
        os.remove(test_config_file_name)

    @staticmethod
    def __create_wrong_configuration_file():
        f = open(test_wrong_config_file_name, "a")
        f.write(test_wrong_config_file_content)
        f.close()

    @staticmethod
    def __remove_wrong_configuration_files():
        os.remove(test_wrong_config_file_name)
