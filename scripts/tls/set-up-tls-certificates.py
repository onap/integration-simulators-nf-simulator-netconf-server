#!/usr/bin/env python
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

import os
import sys
import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Placeholders definition - this needs to match placeholders in
# tls_keystore.xml, tls_truststore.xml and tls_listen.xml
# Server certification
SERVER_KEY_NAME = "SERVER_KEY_NAME"
SERVER_CERT_NAME = "SERVER_CERT_NAME"
SERVER_CERTIFICATE_HERE = "SERVER_CERTIFICATE_HERE"
SERVER_KEY_HERE = "SERVER_KEY_HERE"
SERVER_PUB_KEY_HERE = "SERVER_PUB_KEY_HERE"
# CA certification
CA_CERT_NAME = "CA_CERT_NAME"
CA_CERTIFICATE_HERE = "CA_CERTIFICATE_HERE"
# Client certification
CLIENT_CERT_NAME = "CLIENT_CERT_NAME"
CLIENT_CERTIFICATE_HERE = "CLIENT_CERTIFICATE_HERE"
CLIENT_FINGERPRINT_HERE = "CLIENT_FINGERPRINT_HERE"


class FileHelper(object):
    @classmethod
    def get_file_contents(cls, filename):
        with open(filename, "r") as f:
            return f.read()

    @classmethod
    def write_file_contents(cls, filename, data):
        with open(filename, "w+") as f:
            f.write(data)


class CertHelper(object):
    @classmethod
    def get_pem_content_stripped(cls, pem_dir, pem_filename):
        cmd = "cat {}/{} | grep -v '^-'".format(pem_dir, pem_filename)
        content = CertHelper.system(cmd)
        return content

    @classmethod
    def get_cert_fingerprint(cls, directory, cert_filename):
        cmd = "openssl x509 -fingerprint -noout -in {}/{} | sed -e " \
              "'s/SHA1 Fingerprint//; s/=//; s/=//p'" \
            .format(directory, cert_filename)
        fingerprint = CertHelper.system(cmd)
        return fingerprint

    @classmethod
    def print_keystore_info(cls, server_cert):
        logger.info("Will use server certificate: " + server_cert)

    @classmethod
    def print_truststore_info(cls, ca_cert):
        logger.info("Will use CA certificate: " + ca_cert)

    @classmethod
    def print_listener_info(cls, ca_fingerprint):
        logger.info("CA certificate fingerprint: " + ca_fingerprint)

    @classmethod
    def system(cls, cmd):
        return os.popen(cmd).read().replace("\n", "")


class CertificationData(object):

    def __init__(self,
                 cert_dir, ca_cert_filename,
                 server_cert_filename, server_key_filename, server_pub_key_filename,
                 client_cert_filename,
                 tls_keystore_xml_file, tls_truststore_xml_file, tls_listen_xml_file
                 ):
        self.cert_dir = cert_dir
        self.ca_cert_filename = ca_cert_filename
        self.server_cert_filename = server_cert_filename
        self.server_key_filename = server_key_filename
        self.server_pub_key_filename = server_pub_key_filename
        self.client_cert_filename = client_cert_filename
        self.tls_keystore_xml_file = tls_keystore_xml_file
        self.tls_truststore_xml_file = tls_truststore_xml_file
        self.tls_listen_xml_file = tls_listen_xml_file


class TlsConfigurationPatcher(object):

    def __init__(self, certification_data):
        self.certification_data = certification_data

    def patch_configuration(self):
        server_cert_name, server_key_name, ca_cert_name, client_cert_name = self.__load_names()
        server_cert, server_key, server_pub_key = self.__load_server_data()
        client_cert, client_fingerprint = self.__load_client_data()
        ca_cert = self.__load_ca_data()

        self.__set_up_keystore(server_cert_name, server_key_name, server_cert, server_key, server_pub_key)
        self.__set_up_truststore(ca_cert_name, client_cert_name, ca_cert, client_cert)
        self.__set_up_listener(server_cert_name, server_key_name, ca_cert_name, client_cert_name, client_fingerprint)

    def __load_names(self):
        server_cert_name = self.certification_data.server_cert_filename.replace(".crt", "")
        server_key_name = self.certification_data.server_key_filename.replace(".key", "")
        ca_cert_name = self.certification_data.ca_cert_filename.replace(".crt", "")
        client_cert_name = self.certification_data.client_cert_filename.replace(".crt", "")
        return server_cert_name, server_key_name, ca_cert_name, client_cert_name

    def __load_server_data(self):
        server_cert = CertHelper.get_pem_content_stripped(
            self.certification_data.cert_dir, self.certification_data.server_cert_filename)
        server_key = CertHelper.get_pem_content_stripped(
            self.certification_data.cert_dir, self.certification_data.server_key_filename)
        server_pub_key = CertHelper.get_pem_content_stripped(
            self.certification_data.cert_dir, self.certification_data.server_pub_key_filename)
        return server_cert, server_key, server_pub_key

    def __load_client_data(self):
        client_cert = CertHelper.get_pem_content_stripped(
            self.certification_data.cert_dir, self.certification_data.client_cert_filename)
        client_fingerprint = CertHelper.get_cert_fingerprint(
            self.certification_data.cert_dir, self.certification_data.client_cert_filename)
        return client_cert, client_fingerprint

    def __load_ca_data(self):
        ca_cert = CertHelper.get_pem_content_stripped(
            self.certification_data.cert_dir, self.certification_data.ca_cert_filename)
        return ca_cert

    def __set_up_keystore(self,
                          server_cert_name, server_key_name,
                          server_cert, server_key, server_pub_key):
        CertHelper.print_keystore_info(server_cert)

        # path tls configuration xml file for keystore
        data_srv = FileHelper.get_file_contents(self.certification_data.tls_keystore_xml_file)
        patched_srv = self.__patch_keystore_configuration(
            data_srv, server_key_name, server_cert_name, server_cert, server_key, server_pub_key)
        FileHelper.write_file_contents(self.certification_data.tls_keystore_xml_file, patched_srv)

    def __set_up_truststore(self,
                            ca_cert_name, client_cert_name,
                            ca_cert, client_cert):
        CertHelper.print_truststore_info(ca_cert)

        # path tls configuration xml file for truststore
        data_srv = FileHelper.get_file_contents(self.certification_data.tls_truststore_xml_file)
        patched_srv = self.__patch_truststore_configuration(
            data_srv, ca_cert_name, client_cert_name, ca_cert, client_cert)
        FileHelper.write_file_contents(self.certification_data.tls_truststore_xml_file, patched_srv)

    def __set_up_listener(self,
                          server_cert_name, server_key_name, ca_cert_name, client_cert_name,
                          client_fingerprint):
        CertHelper.print_listener_info(client_fingerprint)

        # path tls configuration xml file for listener
        data_srv = FileHelper.get_file_contents(self.certification_data.tls_listen_xml_file)
        patched_srv = self.__patch_listener_configuration(
            data_srv, ca_cert_name, client_cert_name, server_key_name, server_cert_name, client_fingerprint)
        FileHelper.write_file_contents(self.certification_data.tls_listen_xml_file, patched_srv)

    @classmethod
    def __patch_keystore_configuration(cls, data,
                                       server_key_name, server_cert_name,
                                       server_cert, server_key, server_pub_key):
        data = data.replace(SERVER_KEY_NAME, server_key_name)
        data = data.replace(SERVER_CERT_NAME, server_cert_name)
        data = data.replace(SERVER_CERTIFICATE_HERE, server_cert)
        data = data.replace(SERVER_KEY_HERE, server_key)
        data = data.replace(SERVER_PUB_KEY_HERE, server_pub_key)
        return data

    @classmethod
    def __patch_truststore_configuration(cls, data,
                                         ca_cert_name, client_cert_name,
                                         ca_cert, client_cert):
        data = data.replace(CA_CERT_NAME, ca_cert_name)
        data = data.replace(CLIENT_CERT_NAME, client_cert_name)
        data = data.replace(CLIENT_CERTIFICATE_HERE, client_cert)
        data = data.replace(CA_CERTIFICATE_HERE, ca_cert)
        return data

    @classmethod
    def __patch_listener_configuration(cls, data,
                                       ca_cert_name, client_cert_name, server_key_name, server_cert_name,
                                       client_fingerprint):
        data = data.replace(CA_CERT_NAME, ca_cert_name)
        data = data.replace(CLIENT_CERT_NAME, client_cert_name)
        data = data.replace(SERVER_KEY_NAME, server_key_name)
        data = data.replace(SERVER_CERT_NAME, server_cert_name)
        data = data.replace(CLIENT_FINGERPRINT_HERE, client_fingerprint)
        return data


def main():
    if len(sys.argv) == 10:

        certification_data = CertificationData(
            sys.argv[1],
            sys.argv[2], sys.argv[3], sys.argv[4],
            sys.argv[5],
            sys.argv[6],
            sys.argv[7], sys.argv[8], sys.argv[9],
        )
        configuration_loader = TlsConfigurationPatcher(certification_data)
        configuration_loader.patch_configuration()
        logger.info("XML files patched successfully")

    else:
        logger.error("Usage: %s <cert_dir> <ca_cert_filename> <server_cert_filename> "
                     "<server_key_filename> <server_public_key_filename> <client_cert_filename>"
                     "<load_keystore_xml_full_path> <load_truststore_xml_full_path> <tls_listen_full_path>"
                     % sys.argv[0])
        return 1


if __name__ == '__main__':
    main()
