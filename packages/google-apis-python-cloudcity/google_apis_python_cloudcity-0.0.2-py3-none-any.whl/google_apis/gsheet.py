from google_apis.google_api import GoogleAPI


class GSheet(GoogleAPI):
    """
    This class is to instanciate the Google Sheet API
    https://developers.google.com/sheets/api/reference/rest

    """

    def __init__(self, service_account_key=None, credentials=None, scopes=None):
        self.scopes = scopes if scopes else ['https://www.googleapis.com/auth/spreadsheets']
        self.api_name = 'sheets'
        self.api_version = 'v4'
        super().__init__(self.scopes, self.api_name, self.api_version, service_account_key, credentials)


