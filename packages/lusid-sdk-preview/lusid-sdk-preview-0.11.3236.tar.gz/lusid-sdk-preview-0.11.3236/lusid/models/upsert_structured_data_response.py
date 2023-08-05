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

class UpsertStructuredDataResponse(object):
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
        'href': 'str',
        'values': 'dict(str, datetime)',
        'failed': 'dict(str, ErrorDetail)',
        'links': 'list[Link]'
    }

    attribute_map = {
        'href': 'href',
        'values': 'values',
        'failed': 'failed',
        'links': 'links'
    }

    required_map = {
        'href': 'optional',
        'values': 'optional',
        'failed': 'optional',
        'links': 'optional'
    }

    def __init__(self, href=None, values=None, failed=None, links=None):  # noqa: E501
        """
        UpsertStructuredDataResponse - a model defined in OpenAPI

        :param href:  The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.
        :type href: str
        :param values:  The set of values that were successfully retrieved.
        :type values: dict(str, datetime)
        :param failed:  The set of values that could not be retrieved due along with a reason for this, e.g badly formed request.
        :type failed: dict[str, lusid.ErrorDetail]
        :param links: 
        :type links: list[lusid.Link]

        """  # noqa: E501

        self._href = None
        self._values = None
        self._failed = None
        self._links = None
        self.discriminator = None

        self.href = href
        self.values = values
        self.failed = failed
        self.links = links

    @property
    def href(self):
        """Gets the href of this UpsertStructuredDataResponse.  # noqa: E501

        The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.  # noqa: E501

        :return: The href of this UpsertStructuredDataResponse.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this UpsertStructuredDataResponse.

        The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.  # noqa: E501

        :param href: The href of this UpsertStructuredDataResponse.  # noqa: E501
        :type: str
        """

        self._href = href

    @property
    def values(self):
        """Gets the values of this UpsertStructuredDataResponse.  # noqa: E501

        The set of values that were successfully retrieved.  # noqa: E501

        :return: The values of this UpsertStructuredDataResponse.  # noqa: E501
        :rtype: dict(str, datetime)
        """
        return self._values

    @values.setter
    def values(self, values):
        """Sets the values of this UpsertStructuredDataResponse.

        The set of values that were successfully retrieved.  # noqa: E501

        :param values: The values of this UpsertStructuredDataResponse.  # noqa: E501
        :type: dict(str, datetime)
        """

        self._values = values

    @property
    def failed(self):
        """Gets the failed of this UpsertStructuredDataResponse.  # noqa: E501

        The set of values that could not be retrieved due along with a reason for this, e.g badly formed request.  # noqa: E501

        :return: The failed of this UpsertStructuredDataResponse.  # noqa: E501
        :rtype: dict(str, ErrorDetail)
        """
        return self._failed

    @failed.setter
    def failed(self, failed):
        """Sets the failed of this UpsertStructuredDataResponse.

        The set of values that could not be retrieved due along with a reason for this, e.g badly formed request.  # noqa: E501

        :param failed: The failed of this UpsertStructuredDataResponse.  # noqa: E501
        :type: dict(str, ErrorDetail)
        """

        self._failed = failed

    @property
    def links(self):
        """Gets the links of this UpsertStructuredDataResponse.  # noqa: E501


        :return: The links of this UpsertStructuredDataResponse.  # noqa: E501
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this UpsertStructuredDataResponse.


        :param links: The links of this UpsertStructuredDataResponse.  # noqa: E501
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
        if not isinstance(other, UpsertStructuredDataResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
