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

if [ "$#" -ge 1 ]; then

  ## Set up variable
  SCRIPTS_DIR=$PWD/"$(dirname $0)"
  enable_tls=${ENABLE_TLS:-false}
  models_configuration_file_name=${MODELS_CONFIGURATION_FILE_NAME:-models-configuration.ini}

  ## Install all modules from given directory
  $SCRIPTS_DIR/install-all-module-from-directory.sh $1

  ## If TLS is enabled start initializing certificates
  if [[ "$enable_tls" == "true" ]]; then
    if [ "$#" -ge 2 ]; then
      echo "initializing TLS"
      $SCRIPTS_DIR/install-tls-with-custom-certificates.sh  $SCRIPTS_DIR/tls $2
    else
      echo "Missing second argument: path to file with certificates for TLS."
    fi
  fi

  ## Run netconf server application
  $SCRIPTS_DIR/run-netconf-server-application.sh $1 $models_configuration_file_name

  ## Run sysrepo supervisor
  /usr/bin/supervisord -c /etc/supervisord.conf

else
  echo "Missing first argument: path to file with YANG models."
fi
