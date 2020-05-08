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


class OpenDataServiceException(Exception):
    """Generic exception for open data service layer"""

    def __init__(self, msg, original_exception):
        super(OpenDataServiceException, self).__init__(
            msg + (": %s" % original_exception)
        )
        self.original_exception = original_exception


class OperationMonitoringError(OpenDataServiceException):
    """Exception for errors linked to Operation Monitoring API"""

    def __init__(self, original_exception, line_id, stop_id):
        super(OperationMonitoringError, self).__init__(
            "Error getting arrival times for line [{}] at stop [{}]".format(
                line_id, stop_id
            ),
            original_exception,
        )
        self.line_id = line_id
        self.stop_id = stop_id


class NetworkDescriptionError(OpenDataServiceException):
    """Exception for Network Description API errors"""

    def __init__(self, original_exception, line_id):
        super(NetworkDescriptionError, self).__init__(
            "Error getting line details for line [{}]".format(line_id),
            original_exception,
        )
        self.line_id = line_id


class GTFSDataError(OpenDataServiceException):
    """Exception for GTFS data API errors"""

    def __init__(self, msg, original_exception):
        super(GTFSDataError, self).__init__(msg, original_exception)
