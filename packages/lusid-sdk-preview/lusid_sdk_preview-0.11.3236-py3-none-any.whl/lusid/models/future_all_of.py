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

class FutureAllOf(object):
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
        'start_date': 'datetime',
        'maturity_date': 'datetime',
        'identifiers': 'dict(str, str)',
        'contract_details': 'FuturesContractDetails',
        'contracts': 'float',
        'ref_spot_price': 'float',
        'underlying': 'LusidInstrument',
        'instrument_type': 'str'
    }

    attribute_map = {
        'start_date': 'startDate',
        'maturity_date': 'maturityDate',
        'identifiers': 'identifiers',
        'contract_details': 'contractDetails',
        'contracts': 'contracts',
        'ref_spot_price': 'refSpotPrice',
        'underlying': 'underlying',
        'instrument_type': 'instrumentType'
    }

    required_map = {
        'start_date': 'required',
        'maturity_date': 'required',
        'identifiers': 'required',
        'contract_details': 'required',
        'contracts': 'optional',
        'ref_spot_price': 'optional',
        'underlying': 'required',
        'instrument_type': 'required'
    }

    def __init__(self, start_date=None, maturity_date=None, identifiers=None, contract_details=None, contracts=None, ref_spot_price=None, underlying=None, instrument_type=None):  # noqa: E501
        """
        FutureAllOf - a model defined in OpenAPI

        :param start_date:  The start date of the instrument. This is normally synonymous with the trade-date. (required)
        :type start_date: datetime
        :param maturity_date:  The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.              For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as              Constant Maturity Swaps (CMS) often have sensitivities to rates beyond their last payment date (required)
        :type maturity_date: datetime
        :param identifiers:  external market codes and identifiers for the bond, e.g. ISIN. (required)
        :type identifiers: dict(str, str)
        :param contract_details:  (required)
        :type contract_details: lusid.FuturesContractDetails
        :param contracts:  The number of contracts held
        :type contracts: float
        :param ref_spot_price:  The reference spot price for the future at which the contract was entered into.
        :type ref_spot_price: float
        :param underlying:  (required)
        :type underlying: lusid.LusidInstrument
        :param instrument_type:  The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CashSettled, CdsIndex, Basket, FundingLeg, CrossCurrencySwap, FxSwap (required)
        :type instrument_type: str

        """  # noqa: E501

        self._start_date = None
        self._maturity_date = None
        self._identifiers = None
        self._contract_details = None
        self._contracts = None
        self._ref_spot_price = None
        self._underlying = None
        self._instrument_type = None
        self.discriminator = None

        self.start_date = start_date
        self.maturity_date = maturity_date
        self.identifiers = identifiers
        self.contract_details = contract_details
        if contracts is not None:
            self.contracts = contracts
        if ref_spot_price is not None:
            self.ref_spot_price = ref_spot_price
        self.underlying = underlying
        self.instrument_type = instrument_type

    @property
    def start_date(self):
        """Gets the start_date of this FutureAllOf.  # noqa: E501

        The start date of the instrument. This is normally synonymous with the trade-date.  # noqa: E501

        :return: The start_date of this FutureAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this FutureAllOf.

        The start date of the instrument. This is normally synonymous with the trade-date.  # noqa: E501

        :param start_date: The start_date of this FutureAllOf.  # noqa: E501
        :type: datetime
        """
        if start_date is None:
            raise ValueError("Invalid value for `start_date`, must not be `None`")  # noqa: E501

        self._start_date = start_date

    @property
    def maturity_date(self):
        """Gets the maturity_date of this FutureAllOf.  # noqa: E501

        The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.              For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as              Constant Maturity Swaps (CMS) often have sensitivities to rates beyond their last payment date  # noqa: E501

        :return: The maturity_date of this FutureAllOf.  # noqa: E501
        :rtype: datetime
        """
        return self._maturity_date

    @maturity_date.setter
    def maturity_date(self, maturity_date):
        """Sets the maturity_date of this FutureAllOf.

        The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.              For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as              Constant Maturity Swaps (CMS) often have sensitivities to rates beyond their last payment date  # noqa: E501

        :param maturity_date: The maturity_date of this FutureAllOf.  # noqa: E501
        :type: datetime
        """
        if maturity_date is None:
            raise ValueError("Invalid value for `maturity_date`, must not be `None`")  # noqa: E501

        self._maturity_date = maturity_date

    @property
    def identifiers(self):
        """Gets the identifiers of this FutureAllOf.  # noqa: E501

        external market codes and identifiers for the bond, e.g. ISIN.  # noqa: E501

        :return: The identifiers of this FutureAllOf.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._identifiers

    @identifiers.setter
    def identifiers(self, identifiers):
        """Sets the identifiers of this FutureAllOf.

        external market codes and identifiers for the bond, e.g. ISIN.  # noqa: E501

        :param identifiers: The identifiers of this FutureAllOf.  # noqa: E501
        :type: dict(str, str)
        """
        if identifiers is None:
            raise ValueError("Invalid value for `identifiers`, must not be `None`")  # noqa: E501

        self._identifiers = identifiers

    @property
    def contract_details(self):
        """Gets the contract_details of this FutureAllOf.  # noqa: E501


        :return: The contract_details of this FutureAllOf.  # noqa: E501
        :rtype: FuturesContractDetails
        """
        return self._contract_details

    @contract_details.setter
    def contract_details(self, contract_details):
        """Sets the contract_details of this FutureAllOf.


        :param contract_details: The contract_details of this FutureAllOf.  # noqa: E501
        :type: FuturesContractDetails
        """
        if contract_details is None:
            raise ValueError("Invalid value for `contract_details`, must not be `None`")  # noqa: E501

        self._contract_details = contract_details

    @property
    def contracts(self):
        """Gets the contracts of this FutureAllOf.  # noqa: E501

        The number of contracts held  # noqa: E501

        :return: The contracts of this FutureAllOf.  # noqa: E501
        :rtype: float
        """
        return self._contracts

    @contracts.setter
    def contracts(self, contracts):
        """Sets the contracts of this FutureAllOf.

        The number of contracts held  # noqa: E501

        :param contracts: The contracts of this FutureAllOf.  # noqa: E501
        :type: float
        """

        self._contracts = contracts

    @property
    def ref_spot_price(self):
        """Gets the ref_spot_price of this FutureAllOf.  # noqa: E501

        The reference spot price for the future at which the contract was entered into.  # noqa: E501

        :return: The ref_spot_price of this FutureAllOf.  # noqa: E501
        :rtype: float
        """
        return self._ref_spot_price

    @ref_spot_price.setter
    def ref_spot_price(self, ref_spot_price):
        """Sets the ref_spot_price of this FutureAllOf.

        The reference spot price for the future at which the contract was entered into.  # noqa: E501

        :param ref_spot_price: The ref_spot_price of this FutureAllOf.  # noqa: E501
        :type: float
        """

        self._ref_spot_price = ref_spot_price

    @property
    def underlying(self):
        """Gets the underlying of this FutureAllOf.  # noqa: E501


        :return: The underlying of this FutureAllOf.  # noqa: E501
        :rtype: LusidInstrument
        """
        return self._underlying

    @underlying.setter
    def underlying(self, underlying):
        """Sets the underlying of this FutureAllOf.


        :param underlying: The underlying of this FutureAllOf.  # noqa: E501
        :type: LusidInstrument
        """
        if underlying is None:
            raise ValueError("Invalid value for `underlying`, must not be `None`")  # noqa: E501

        self._underlying = underlying

    @property
    def instrument_type(self):
        """Gets the instrument_type of this FutureAllOf.  # noqa: E501

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CashSettled, CdsIndex, Basket, FundingLeg, CrossCurrencySwap, FxSwap  # noqa: E501

        :return: The instrument_type of this FutureAllOf.  # noqa: E501
        :rtype: str
        """
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, instrument_type):
        """Sets the instrument_type of this FutureAllOf.

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CashSettled, CdsIndex, Basket, FundingLeg, CrossCurrencySwap, FxSwap  # noqa: E501

        :param instrument_type: The instrument_type of this FutureAllOf.  # noqa: E501
        :type: str
        """
        if instrument_type is None:
            raise ValueError("Invalid value for `instrument_type`, must not be `None`")  # noqa: E501
        allowed_values = ["QuotedSecurity", "InterestRateSwap", "FxForward", "Future", "ExoticInstrument", "FxOption", "CreditDefaultSwap", "InterestRateSwaption", "Bond", "EquityOption", "FixedLeg", "FloatingLeg", "BespokeCashFlowsLeg", "Unknown", "TermDeposit", "ContractForDifference", "EquitySwap", "CashPerpetual", "CashSettled", "CdsIndex", "Basket", "FundingLeg", "CrossCurrencySwap", "FxSwap"]  # noqa: E501
        if instrument_type not in allowed_values:
            raise ValueError(
                "Invalid value for `instrument_type` ({0}), must be one of {1}"  # noqa: E501
                .format(instrument_type, allowed_values)
            )

        self._instrument_type = instrument_type

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
        if not isinstance(other, FutureAllOf):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
