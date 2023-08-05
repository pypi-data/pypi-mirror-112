# Copyright 2021 ADTRAN, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
from grpc_robot.grpc_robot import _package_version_get

from voltha_protos import events_pb2
from voltha_protos import tech_profile_pb2
from grpc_robot.tools.protobuf_to_dict import protobuf_to_dict


class VolthaTools(object):
    """
    Tools for the voltha, e.g decoding / conversions.
    """

    try:
        ROBOT_LIBRARY_VERSION = _package_version_get('grpc_robot')
    except NameError:
        ROBOT_LIBRARY_VERSION = 'unknown'

    @staticmethod
    def events_decode_event(bytestring, return_enum_integer='false', return_defaults='false', human_readable_timestamps='true'):
        """
        Converts bytes to an Event as defined in _message Event_ from events.proto

        *Parameters*:
        - bytestring: <bytes>; Byte string, e.g. as it comes from Kafka messages.
        - return_enum_integer: <string> or <bool>; Whether or not to return the enum values as integer values rather than their labels. Default: _false_.
        - return_defaults: <string> or <bool>; Whether or not to return the default values. Default: _false_.
        - human_readable_timestamps: <string> or <bool>; Whether or not to convert the timestamps to human-readable format. Default: _true_.

        *Return*: A dictionary with _event_ structure.

        *Example*:
        | Import Library | grpc_robot.VolthaTools | WITH NAME | voltha_tools |
        | ${kafka_records} | kafka.Records Get |
        | FOR | ${kafka_record} | IN | @{kafka_records} |
        |  | ${event} | voltha_tools.Events Decode Event | ${kafka_record}[message] |
        |  | Log | ${event} |
        | END |
        """
        return_enum_integer = str(return_enum_integer).lower() == 'true'
        result = events_pb2.Event.FromString(bytestring)
        return protobuf_to_dict(result,
                                use_enum_labels=not return_enum_integer,
                                including_default_value_fields=str(return_defaults).lower() == 'true',
                                human_readable_timestamps=str(human_readable_timestamps).lower() == 'true')

    @staticmethod
    def tech_profile_decode_resource_instance(bytestring, return_enum_integer='false', return_defaults='false', human_readable_timestamps='true'):
        """
        Converts bytes to an resource instance as defined in _message ResourceInstance_ from tech_profile.proto

        *Parameters*:
        - bytestring: <bytes>; Byte string, e.g. as it comes from Kafka messages.
        - return_enum_integer: <string> or <bool>; Whether or not to return the enum values as integer values rather than their labels. Default: _false_.
        - return_defaults: <string> or <bool>; Whether or not to return the default values. Default: _false_.
        - human_readable_timestamps: <string> or <bool>; Whether or not to convert the timestamps to human-readable format. Default: _true_.

        *Return*: A dictionary with _event_ structure.

        *Example*:
        | Import Library | grpc_robot.VolthaTools | WITH NAME | voltha_tools |
        | ${kafka_records} | kafka.Records Get |
        | FOR | ${kafka_record} | IN | @{kafka_records} |
        |  | ${event} | voltha_tools. Tech Profile Decode Resource Instance | ${kafka_record}[message] |
        |  | Log | ${event} |
        | END |
        """
        return_enum_integer = str(return_enum_integer).lower() == 'true'
        result = tech_profile_pb2.ResourceInstance.FromString(bytestring)
        return protobuf_to_dict(result,
                                use_enum_labels=not return_enum_integer,
                                including_default_value_fields=str(return_defaults).lower() == 'true',
                                human_readable_timestamps=str(human_readable_timestamps).lower() == 'true')


if __name__ == '__main__':
    message = b"\x08\x40\x12\x07\x58\x47\x53\x2d\x50\x4f\x4e\x1a\x42\x6f\x6c\x74\x2d\x7b\x39\x35\x36\x31\x37\x31\x32\x62\x2d\x35\x33\x32\x33\x2d\x34\x64\x64\x63\x2d\x38\x36\x62\x34\x2d\x64\x35\x31\x62\x62\x34\x61\x65\x30\x37\x33\x39\x7d\x2f\x70\x6f\x6e\x2d\x7b\x31\x7d\x2f\x6f\x6e\x75\x2d\x7b\x32\x7d\x2f\x75\x6e\x69\x2d\x7b\x30\x7d\x20\x81\x08\x2a\x10\x88\x08\x89\x08\x8a\x08\x8b\x08\x8c\x08\x8d\x08\x8e\x08\x8f\x08"
    print(VolthaTools.tech_profile_decode_resource_instance(message))
