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

  ## Set up custom certificates
  python $1/set-up-tls-certificates.py $2 \
           ca.crt server.crt server.key server_pub.key client.crt \
           $1/tls_keystore.xml $1/tls_truststore.xml $1/tls_listen.xml

  ## Configure and start TLS listener
  sysrepocfg --edit=$1/tls_keystore.xml --format=xml --datastore=running --module=ietf-keystore
  sysrepocfg --edit=$1/tls_truststore.xml --format=xml --datastore=running --module=ietf-truststore
  sysrepocfg --edit=$1/tls_listen.xml --format=xml --datastore=running --module=ietf-netconf-server
  sysrepocfg --copy-from=running --datastore=startup

else
  echo "Missing arguments: first argument should be path to file with tls scripts and/ore second argument should be path to file with certificates for TLS."
fi
