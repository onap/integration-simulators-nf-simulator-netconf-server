#!/bin/bash
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

if [ "$#" -eq 2 ]; then

  ## Set up variable
  MODELS_CONFIG_PATH=$1
  MODELS_CONFIG_NAME=$2

  echo "Starting NETCONF Change listener"
  python3 ./application/netconf_change_listener_application.py $MODELS_CONFIG_PATH/$MODELS_CONFIG_NAME &


  echo "Starting NETCONF Rest server"
  python3 ./application/netconf_rest_application.py $MODELS_CONFIG_PATH/$MODELS_CONFIG_NAME &


else
    echo "[ERROR] Invalid number of arguments. Please provide all required arguments."
fi
