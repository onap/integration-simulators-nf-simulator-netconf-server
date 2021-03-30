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
class NetconfAppConfiguration(object):

    @staticmethod
    def get_configuration(args: list):
        if len(args) >= 4:
            configuration_file = args[1]
            kafka_host_name = args[2]
            kafka_port = args[3]
            kafka_topic = args[4]

            return NetconfAppConfiguration(configuration_file, kafka_host_name, int(kafka_port), kafka_topic), None
        else:
            return None, "Invalid number of arguments. Please provide all required arguments."

    def __init__(self, module_configuration_file_path: str, kafka_host_name: str, kafka_port: int, kafka_topic: str):
        self.module_configuration_file_path = module_configuration_file_path
        self.kafka_host_name = kafka_host_name
        self.kafka_port = kafka_port
        self.kafka_topic = kafka_topic

    def __str__(self):
        return "NetconfAppConfiguration[configuration_file -> '{}', " \
               "kafka_host_name -> '{}', kafka_port -> '{}', kafka_topic -> '{}']"\
            .format(self.module_configuration_file_path, self.kafka_host_name, self.kafka_port, self.kafka_topic)

