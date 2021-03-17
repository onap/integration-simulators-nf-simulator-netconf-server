###
# ============LICENSE_START=======================================================
# Simulator
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
import sysrepo


class SysrepoClient(object):

    @staticmethod
    def run_in_session(method_to_run, *extra_args):
        with sysrepo.SysrepoConnection() as connection:
            with connection.start_session() as session:
                method_to_run(session, *extra_args)
