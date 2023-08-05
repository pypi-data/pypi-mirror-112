#-*- coding: utf-8 -*-

from .utils.juno import *

# ENTITIES
from .entities.address import Address
from .entities.accountholder import AccountHolder
from .entities.bankaccount import BankAccount
from .entities.companymembers import CompanyMembers
from .entities.digitalaccount import DigitalAccount
from .entities.legalrepresentative import LegalRepresentative
from .entities.recipient import Recipient
from .entities.transfer import Transfer

# SERVICES
from .services import *
from .services import transfers


# from junopy.entities.amount import Amount
# from junopy.entities.bankdebit import BankDebit
# from junopy.entities.boleto import Boleto
# from junopy.entities.boletoinstructionlines import BoletoInstructionLines
# from junopy.entities.cancellationdetail import CancellationDetail
# from junopy.entities.checkoutpreferences import CheckoutPreferences
# from junopy.entities.creditcard import CreditCard
# from junopy.entities.device import Device
# from junopy.entities.entrie import Entrie
# from junopy.entities.event import Event
# from junopy.entities.fee import Fee
# from junopy.entities.fundinginstrument import FundingInstrument
# from junopy.entities.geolocation import Geolocation
# from junopy.entities.holder import Holder
# from junopy.entities.installments import Installments
# from junopy.entities.moipaccount import MoipAccount
# from junopy.entities.phone import Phone
# from junopy.entities.product import Product
# from junopy.entities.receiver import Receiver
# from junopy.entities.redirecthref import RedirectHref
# from junopy.entities.redirecturls import RedirectUrls
# from junopy.entities.subtotals import Subtotals
# from junopy.entities.taxdocument import TaxDocument
# from junopy.entities.webhook import WebHook
#
