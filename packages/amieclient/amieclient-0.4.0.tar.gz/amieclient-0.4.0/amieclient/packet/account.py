"""
AMIE packets relating to accounts
"""

from .base import Packet, PacketInvalidData
from .validators import _validate_resource_list


class DataAccountCreate(Packet):
    _packet_type = 'data_account_create'
    _expected_reply = [{'type': 'inform_transaction_complete', 'timeout': 30240}]
    _data_keys_required = ['PersonID', 'ProjectID']
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = ['DnList']


class NotifyAccountCreate(Packet):
    _packet_type = 'notify_account_create'
    _expected_reply = [{'type': 'data_account_create', 'timeout': 30240}]
    _data_keys_required = [
        'AccountActivityTime',
        'AcademicDegree',
        'ProjectID',
        'ResourceList',
        'UserFirstName',
        'UserLastName',
        'UserOrganization',
        'UserOrgCode',
        'UserPersonID',
        'UserRemoteSiteLogin',
    ]
    _data_keys_not_required_in_reply = [
        'AcademicDegree',
        'UserFirstName',
        'UserLastName',
        'UserOrganization',
        'UserOrgCode',
        'UserPersonID'
    ]
    _data_keys_allowed = [
        'NsfStatusCode',
        'RoleList',
        'UserBusinessPhoneExtension',
        'UserBusinessPhoneNumber',
        'UserCity',
        'UserCountry',
        'UserDepartment',
        'UserDnList',
        'UserDnList',
        'UserEmail',
        'UserFax',
        'UserGlobalID',
        'UserHomePhoneExtension',
        'UserHomePhoneNumber',
        'UserMiddleName',
        'UserPasswordAccessEnable',
        'UserPosition',
        'UserRequestedLoginList',
        'UserState',
        'UserStreetAddress',
        'UserStreetAddress2',
        'UserTitle',
    ]

    def validate_data(self, raise_on_invalid=False):
        """
        Validates that there is only one element in the ResourceList attribute
        """
        try:
            _validate_resource_list(self)

        except PacketInvalidData as e:
            if raise_on_invalid:
                raise e
            else:
                return False
        return super().validate_data(raise_on_invalid)


class NotifyAccountInactivate(Packet):
    _packet_type = 'notify_account_inactivate'
    _expected_reply = [{'type': 'inform_transaction_complete', 'timeout': 30240}]
    _data_keys_required = ['PersonID', 'ProjectID', 'ResourceList']
    _data_keys_not_required_in_reply = ['PersonID', 'ProjectID', 'ResourceList']
    _data_keys_allowed = ['Comment']

    def validate_data(self, raise_on_invalid=False):
        """
        Validates that there is only one element in the ResourceList attribute
        """
        try:
            _validate_resource_list(self)

        except PacketInvalidData as e:
            if raise_on_invalid:
                raise e
            else:
                return False
        return super().validate_data(raise_on_invalid)


class NotifyAccountReactivate(Packet):
    _packet_type = 'notify_account_reactivate'
    _expected_reply = [{'type': 'inform_transaction_complete', 'timeout': 30240}]
    _data_keys_required = ['PersonID', 'ProjectID', 'ResourceList']
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = ['Comment']

    def validate_data(self, raise_on_invalid=False):
        """
        Validates that there is only one element in the ResourceList attribute
        """
        try:
            _validate_resource_list(self)

        except PacketInvalidData as e:
            if raise_on_invalid:
                raise e
            else:
                return False
        return super().validate_data(raise_on_invalid)


class RequestAccountCreate(Packet):
    _packet_type = 'request_account_create'
    _expected_reply = ['notify_account_create']
    _data_keys_required = [
        'GrantNumber',
        'ResourceList',
        'UserFirstName',
        'UserLastName',
        'UserOrganization',
        'UserOrgCode',
    ]
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = [
        'RoleList',
        'UserGlobalID',
        'AllocatedResource',
        'NsfStatusCode',
        'ProjectID',
        'SitePersonId',
        'AcademicDegree',
        'CitizenshipList',
        'UserBusinessPhoneComment',
        'UserBusinessPhoneExtension',
        'UserBusinessPhoneNumber',
        'UserCity',
        'UserCountry',
        'UserDepartment',
        'UserDnList',
        'UserEmail',
        'UserFax',
        'UserHomePhoneComment',
        'UserHomePhoneExtension',
        'UserHomePhoneNumber',
        'UserMiddleName',
        'UserPasswordAccessEnable',
        'UserPersonID',
        'UserRequestedLoginList',
        'UserState',
        'UserStreetAddress',
        'UserStreetAddress2',
        'UserTitle',
        'UserZip',
    ]

    def validate_data(self, raise_on_invalid=False):
        """
        Validates that there is only one element in the ResourceList attribute
        """
        try:
            _validate_resource_list(self)

        except PacketInvalidData as e:
            if raise_on_invalid:
                raise e
            else:
                return False
        return super().validate_data(raise_on_invalid)


class RequestAccountInactivate(Packet):
    _packet_type = 'request_account_inactivate'
    _expected_reply = [{'type': 'notify_account_inactivate', 'timeout': 30240}]
    _data_keys_required = ['PersonID', 'ProjectID', 'ResourceList']
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = ['Comment']

    def validate_data(self, raise_on_invalid=False):
        """
        Validates that there is only one element in the ResourceList attribute
        """
        try:
            _validate_resource_list(self)

        except PacketInvalidData as e:
            if raise_on_invalid:
                raise e
            else:
                return False
        return super().validate_data(raise_on_invalid)


class RequestAccountReactivate(Packet):
    _packet_type = 'request_account_reactivate'
    _expected_reply = [{'type': 'notify_account_reactivate', 'timeout': 30240}]
    _data_keys_required = ['PersonID', 'ProjectID', 'ResourceList']
    _data_keys_not_required_in_reply = []
    _data_keys_allowed = ['Comment']

    def validate_data(self, raise_on_invalid=False):
        """
        Validates that there is only one element in the ResourceList attribute
        """
        try:
            _validate_resource_list(self)

        except PacketInvalidData as e:
            if raise_on_invalid:
                raise e
            else:
                return False
        return super().validate_data(raise_on_invalid)
