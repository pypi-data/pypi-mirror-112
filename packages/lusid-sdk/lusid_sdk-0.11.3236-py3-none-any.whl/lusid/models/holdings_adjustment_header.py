# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.3236
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

class HoldingsAdjustmentHeader(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'effective_at': 'datetime',
        'version': 'Version',
        'unmatched_holding_method': 'str',
        'links': 'list[Link]'
    }

    attribute_map = {
        'effective_at': 'effectiveAt',
        'version': 'version',
        'unmatched_holding_method': 'unmatchedHoldingMethod',
        'links': 'links'
    }

    required_map = {
        'effective_at': 'required',
        'version': 'required',
        'unmatched_holding_method': 'required',
        'links': 'optional'
    }

    def __init__(self, effective_at=None, version=None, unmatched_holding_method=None, links=None):  # noqa: E501
        """
        HoldingsAdjustmentHeader - a model defined in OpenAPI

        :param effective_at:  The effective datetime from which the adjustment is valid. There can only be one holdings adjustment for a transaction portfolio at a specific effective datetime, so this uniquely identifies the adjustment. (required)
        :type effective_at: datetime
        :param version:  (required)
        :type version: lusid.Version
        :param unmatched_holding_method:  Describes how the holdings were adjusted. If 'PositionToZero' the entire transaction portfolio's holdings were set via a call to 'Set holdings'. If 'KeepTheSame' only the specified holdings were adjusted via a call to 'Adjust holdings'. The available values are: PositionToZero, KeepTheSame (required)
        :type unmatched_holding_method: str
        :param links: 
        :type links: list[lusid.Link]

        """  # noqa: E501

        self._effective_at = None
        self._version = None
        self._unmatched_holding_method = None
        self._links = None
        self.discriminator = None

        self.effective_at = effective_at
        self.version = version
        self.unmatched_holding_method = unmatched_holding_method
        self.links = links

    @property
    def effective_at(self):
        """Gets the effective_at of this HoldingsAdjustmentHeader.  # noqa: E501

        The effective datetime from which the adjustment is valid. There can only be one holdings adjustment for a transaction portfolio at a specific effective datetime, so this uniquely identifies the adjustment.  # noqa: E501

        :return: The effective_at of this HoldingsAdjustmentHeader.  # noqa: E501
        :rtype: datetime
        """
        return self._effective_at

    @effective_at.setter
    def effective_at(self, effective_at):
        """Sets the effective_at of this HoldingsAdjustmentHeader.

        The effective datetime from which the adjustment is valid. There can only be one holdings adjustment for a transaction portfolio at a specific effective datetime, so this uniquely identifies the adjustment.  # noqa: E501

        :param effective_at: The effective_at of this HoldingsAdjustmentHeader.  # noqa: E501
        :type: datetime
        """
        if effective_at is None:
            raise ValueError("Invalid value for `effective_at`, must not be `None`")  # noqa: E501

        self._effective_at = effective_at

    @property
    def version(self):
        """Gets the version of this HoldingsAdjustmentHeader.  # noqa: E501


        :return: The version of this HoldingsAdjustmentHeader.  # noqa: E501
        :rtype: Version
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this HoldingsAdjustmentHeader.


        :param version: The version of this HoldingsAdjustmentHeader.  # noqa: E501
        :type: Version
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def unmatched_holding_method(self):
        """Gets the unmatched_holding_method of this HoldingsAdjustmentHeader.  # noqa: E501

        Describes how the holdings were adjusted. If 'PositionToZero' the entire transaction portfolio's holdings were set via a call to 'Set holdings'. If 'KeepTheSame' only the specified holdings were adjusted via a call to 'Adjust holdings'. The available values are: PositionToZero, KeepTheSame  # noqa: E501

        :return: The unmatched_holding_method of this HoldingsAdjustmentHeader.  # noqa: E501
        :rtype: str
        """
        return self._unmatched_holding_method

    @unmatched_holding_method.setter
    def unmatched_holding_method(self, unmatched_holding_method):
        """Sets the unmatched_holding_method of this HoldingsAdjustmentHeader.

        Describes how the holdings were adjusted. If 'PositionToZero' the entire transaction portfolio's holdings were set via a call to 'Set holdings'. If 'KeepTheSame' only the specified holdings were adjusted via a call to 'Adjust holdings'. The available values are: PositionToZero, KeepTheSame  # noqa: E501

        :param unmatched_holding_method: The unmatched_holding_method of this HoldingsAdjustmentHeader.  # noqa: E501
        :type: str
        """
        if unmatched_holding_method is None:
            raise ValueError("Invalid value for `unmatched_holding_method`, must not be `None`")  # noqa: E501
        allowed_values = ["PositionToZero", "KeepTheSame"]  # noqa: E501
        if unmatched_holding_method not in allowed_values:
            raise ValueError(
                "Invalid value for `unmatched_holding_method` ({0}), must be one of {1}"  # noqa: E501
                .format(unmatched_holding_method, allowed_values)
            )

        self._unmatched_holding_method = unmatched_holding_method

    @property
    def links(self):
        """Gets the links of this HoldingsAdjustmentHeader.  # noqa: E501


        :return: The links of this HoldingsAdjustmentHeader.  # noqa: E501
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this HoldingsAdjustmentHeader.


        :param links: The links of this HoldingsAdjustmentHeader.  # noqa: E501
        :type: list[Link]
        """

        self._links = links

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, HoldingsAdjustmentHeader):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
