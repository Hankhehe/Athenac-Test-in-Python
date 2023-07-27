from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HostReportLogonUser(_message.Message):
    __slots__ = ["gpo_result", "logon_account", "remote_login"]
    GPO_RESULT_FIELD_NUMBER: _ClassVar[int]
    LOGON_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    REMOTE_LOGIN_FIELD_NUMBER: _ClassVar[int]
    gpo_result: str
    logon_account: str
    remote_login: bool
    def __init__(self, logon_account: _Optional[str] = ..., remote_login: bool = ..., gpo_result: _Optional[str] = ...) -> None: ...

class HostReportReply(_message.Message):
    __slots__ = ["Message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    Message: str
    def __init__(self, Message: _Optional[str] = ...) -> None: ...

class HostReportRequest(_message.Message):
    __slots__ = ["MACs", "domain_name", "host_name", "local_admin_account", "logon_users", "motherboard_serial_number", "os_build", "os_display_product", "os_product", "os_type", "os_version", "pending_hot_fix", "share_folder", "softwares", "timestamp", "windows_hot_fix_last_check_time"]
    DOMAIN_NAME_FIELD_NUMBER: _ClassVar[int]
    HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    LOCAL_ADMIN_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    LOGON_USERS_FIELD_NUMBER: _ClassVar[int]
    MACS_FIELD_NUMBER: _ClassVar[int]
    MACs: _containers.RepeatedScalarFieldContainer[str]
    MOTHERBOARD_SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    OS_BUILD_FIELD_NUMBER: _ClassVar[int]
    OS_DISPLAY_PRODUCT_FIELD_NUMBER: _ClassVar[int]
    OS_PRODUCT_FIELD_NUMBER: _ClassVar[int]
    OS_TYPE_FIELD_NUMBER: _ClassVar[int]
    OS_VERSION_FIELD_NUMBER: _ClassVar[int]
    PENDING_HOT_FIX_FIELD_NUMBER: _ClassVar[int]
    SHARE_FOLDER_FIELD_NUMBER: _ClassVar[int]
    SOFTWARES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    WINDOWS_HOT_FIX_LAST_CHECK_TIME_FIELD_NUMBER: _ClassVar[int]
    domain_name: str
    host_name: str
    local_admin_account: _containers.RepeatedScalarFieldContainer[str]
    logon_users: _containers.RepeatedCompositeFieldContainer[HostReportLogonUser]
    motherboard_serial_number: str
    os_build: str
    os_display_product: str
    os_product: str
    os_type: str
    os_version: str
    pending_hot_fix: _containers.RepeatedScalarFieldContainer[str]
    share_folder: _containers.RepeatedScalarFieldContainer[str]
    softwares: _containers.RepeatedCompositeFieldContainer[Software]
    timestamp: _timestamp_pb2.Timestamp
    windows_hot_fix_last_check_time: _timestamp_pb2.Timestamp
    def __init__(self, host_name: _Optional[str] = ..., MACs: _Optional[_Iterable[str]] = ..., domain_name: _Optional[str] = ..., logon_users: _Optional[_Iterable[_Union[HostReportLogonUser, _Mapping]]] = ..., os_type: _Optional[str] = ..., os_product: _Optional[str] = ..., share_folder: _Optional[_Iterable[str]] = ..., pending_hot_fix: _Optional[_Iterable[str]] = ..., windows_hot_fix_last_check_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., local_admin_account: _Optional[_Iterable[str]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., motherboard_serial_number: _Optional[str] = ..., softwares: _Optional[_Iterable[_Union[Software, _Mapping]]] = ..., os_display_product: _Optional[str] = ..., os_build: _Optional[str] = ..., os_version: _Optional[str] = ...) -> None: ...

class Software(_message.Message):
    __slots__ = ["DisplayName", "DisplayVersion", "EstimatedSize", "InstallDate", "Publisher"]
    DISPLAYNAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAYVERSION_FIELD_NUMBER: _ClassVar[int]
    DisplayName: str
    DisplayVersion: str
    ESTIMATEDSIZE_FIELD_NUMBER: _ClassVar[int]
    EstimatedSize: str
    INSTALLDATE_FIELD_NUMBER: _ClassVar[int]
    InstallDate: str
    PUBLISHER_FIELD_NUMBER: _ClassVar[int]
    Publisher: str
    def __init__(self, DisplayName: _Optional[str] = ..., DisplayVersion: _Optional[str] = ..., Publisher: _Optional[str] = ..., InstallDate: _Optional[str] = ..., EstimatedSize: _Optional[str] = ...) -> None: ...
