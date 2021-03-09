#!/bin/sh
###
# ============LICENSE_START=======================================================
# Netconf-server
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

## Set up certs path
cert_path="."
if [ "$#" -eq 1 ]; then
  cert_path=$1
fi
cd $cert_path

## Generate self-signed CA cert and key
openssl req -nodes -newkey rsa:2048 -keyout ca.key -out ca.csr -subj "/C=US/O=ONAP/OU=OSAAF/CN=CA.NETCONF/"
openssl x509 -req -in ca.csr -signkey ca.key -days 730 -out ca.crt
rm ca.csr

## Generate Server cert and key
openssl req -nodes -newkey rsa:2048 -keyout server.key -out server.csr -subj "/C=US/O=ONAP/OU=OSAAF/CN=CA.NETCONF.SERVER/"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 730 -sha256
openssl x509 -pubkey -noout -in server.crt  > server_pub.key
rm server.csrsrl

## Generate Client cert and key
openssl req -nodes -newkey rsa:2048 -keyout client.key -out client.csr -subj "/C=US/O=ONAP/OU=OSAAF/CN=CA.NETCONF.CLIENT/"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 730 -sha256
rm client.csr
