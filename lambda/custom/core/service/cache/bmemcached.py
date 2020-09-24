#   Copyright 2020 Antonin Jousson
#
#  Licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  or in the "license" file accompanying this file. This file is
#  distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
#  OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the
#  License.

import bmemcached
from hermes.backend import memcached


class BmemcachedBackend(memcached.Backend):
    @property
    def client(self):
        if not hasattr(self._local, "client"):
            self._local.client = bmemcached.Client(**self._options)

        return self._local.client
