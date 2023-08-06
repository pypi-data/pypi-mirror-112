import os.path

from google_apis.google_api import GoogleAPI


class ManufacturerCenter(GoogleAPI):
    """
    This class is to instanciate the Double Click Bid manager API
    https://developers.google.com/bid-manager/v1.1

    Note: This API is used to interact with the reporting functionality

    """

    def __init__(self, service_account_key=None, credentials=None):
        self.scopes = ['https://www.googleapis.com/auth/manufacturercenter']
        self.api_name = 'manufacturers'
        self.api_version = 'v1'
        super().__init__(self.scopes, self.api_name, self.api_version, service_account_key, credentials)

