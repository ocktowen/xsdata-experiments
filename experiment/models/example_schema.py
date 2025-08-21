from __future__ import annotations

from decimal import Decimal
from typing import ForwardRef

from pydantic import BaseModel, ConfigDict
from xsdata_pydantic.fields import field

from experiment.mixins import XMLDummyMixin


class AddressType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    street_name: str = field(
        metadata={
            "name": "StreetName",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    building_number: None | str = field(
        default=None,
        metadata={
            "name": "BuildingNumber",
            "type": "Element",
            "namespace": "",
        },
    )
    city: str = field(
        metadata={
            "name": "City",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    country: str = field(
        metadata={
            "name": "Country",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )


class Payment(BaseModel):
    model_config = ConfigDict(defer_build=True)
    debit: list[Payment.Debit] = field(
        default_factory=list,
        metadata={
            "name": "Debit",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )
    credit: list[Payment.Credit] = field(
        default_factory=list,
        metadata={
            "name": "Credit",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )

    class Debit(BaseModel):
        model_config = ConfigDict(defer_build=True)
        payment_id: str = field(
            metadata={
                "name": "PaymentID",
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        description: Decimal = field(
            metadata={
                "name": "Description",
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        debit_amount: Decimal = field(
            metadata={
                "name": "DebitAmount",
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )

    class Credit(BaseModel):
        model_config = ConfigDict(defer_build=True)
        payment_id: str = field(
            metadata={
                "name": "PaymentID",
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        description: Decimal = field(
            metadata={
                "name": "Description",
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        credit_amount: Decimal = field(
            metadata={
                "name": "CreditAmount",
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )


class WorkAddress(AddressType):
    pass
    model_config = ConfigDict(defer_build=True)


class Customer(BaseModel):
    model_config = ConfigDict(defer_build=True)
    name: str = field(
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    work_address: list[WorkAddress] = field(
        default_factory=list,
        metadata={
            "name": "WorkAddress",
            "type": "Element",
        },
    )
    home_address: list[AddressType] = field(
        default_factory=list,
        metadata={
            "name": "HomeAddress",
            "type": "Element",
            "namespace": "",
        },
    )
    choice: list[Customer.ShipToAddress | Customer.BillingAddress] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "ShipToAddress",
                    "type": ForwardRef("Customer.ShipToAddress"),
                    "namespace": "",
                },
                {
                    "name": "BillingAddress",
                    "type": ForwardRef("Customer.BillingAddress"),
                    "namespace": "",
                },
            ),
        },
    )

    class ShipToAddress(AddressType):
        pass
        model_config = ConfigDict(defer_build=True)

    class BillingAddress(AddressType):
        pass
        model_config = ConfigDict(defer_build=True)


class ExampleFile(BaseModel, XMLDummyMixin):
    model_config = ConfigDict(defer_build=True)
    customer: list[Customer] = field(
        default_factory=list,
        metadata={
            "name": "Customer",
            "type": "Element",
        },
    )
    payment: list[Payment] = field(
        default_factory=list,
        metadata={
            "name": "Payment",
            "type": "Element",
        },
    )
