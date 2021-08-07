import requests

from enum import Enum
from errors import AppStoreValidationError
from requests.exceptions import RequestException


class AppStoreValidationServer(Enum):
    SANDBOX = "https://sandbox.itunes.apple.com/verifyReceipt"
    PRODUCTION = "https://buy.itunes.apple.com/verifyReceipt"


class AppStoreReceiptValidator:
    def __init__(
        self,
        validation_server: AppStoreValidationServer = AppStoreValidationServer.SANDBOX,
    ):
        """ AppStoreReceiptValidator constructor.

        :param validationServer:
        """
        self.validation_server = validation_server

    def prepare_receipt(
        self,
        receipt: str,
        shared_secret: str
    ) -> dict:
        """
        """

        body = {"receipt-data": receipt}

        if shared_secret:
            body["password"] = shared_secret

        return body

    def post_request(
        self,
        data: dict
    ) -> dict:
        """
        """

        try:
            return requests.post(self.validation_server.value, json=data).json()
        except (ValueError, RequestException):
            raise AppStoreValidationError("HTTP Error")

    def validate(
        self,
        receipt: str,
        shared_secret: str,
    ):
        prepared_receipt = self.prepare_receipt(receipt, shared_secret)
        json_response = self.post_request(prepared_receipt)
