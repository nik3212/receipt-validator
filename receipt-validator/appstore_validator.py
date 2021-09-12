import requests

from enum import Enum
from errors import AppStoreValidationError
from requests.exceptions import RequestException


errors = {
    21000: AppStoreValidationError('The App Store could not read the JSON object you provided.'),
    21002: AppStoreValidationError('The data in the receipt-data property was malformed or missing.'),
    21003: AppStoreValidationError('The receipt could not be authenticated.'),
    21004: AppStoreValidationError('The shared secret you provided does not match the shared secret on file for your account.'),
    21005: AppStoreValidationError('The receipt server is not currently available.'),
    21006: AppStoreValidationError('This receipt is valid but the subscription has expired. When this status code is returned to your server, the receipt data is also decoded and returned as part of the response.'),
    21007: AppStoreValidationError('This receipt is from the test environment, but it was sent to the production environment for verification. Send it to the test environment instead.'),
    21008: AppStoreValidationError('This receipt is from the production environment, but it was sent to the test environment for verification. Send it to the production environment instead.')
}


class AppStoreValidationServer(Enum):
    SANDBOX = "https://sandbox.itunes.apple.com/verifyReceipt"
    PRODUCTION = "https://buy.itunes.apple.com/verifyReceipt"


class AppStoreReceiptValidator:
    def __init__(
        self,
        validation_server: AppStoreValidationServer = AppStoreValidationServer.SANDBOX,
    ):
        self.validation_server = validation_server

    def prepare_receipt(
        self,
        receipt: str,
        shared_secret: str
    ) -> dict:
        body = {"receipt-data": receipt}

        if shared_secret:
            body["password"] = shared_secret

        return body

    def post_request(
        self,
        data: dict
    ) -> dict:
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

        status = json_response.get("status", "unknown")

        if status in [21007, 21008]:
            self.validation_server = AppStoreValidationServer.SANDBOX if self.validation_server == AppStoreValidationServer.PRODUCTION else AppStoreValidationServer.SANDBOX

            api_response = self.post_request(prepared_receipt)
            status = api_response["status"]

        if status != 0:
            error = errors.get(status, AppStoreValidationError("Unknown API status"))

            raise error

        return json_response
