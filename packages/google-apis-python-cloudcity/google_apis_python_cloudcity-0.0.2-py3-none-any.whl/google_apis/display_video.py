from google_apis.google_api import GoogleAPI

class DisplayVideo(GoogleAPI):
    """
    This class is to instanciate the Double Click Bid manager API
    https://developers.google.com/display-video/api/reference/rest

    Note: This API is used to interact with DV360 entities

    """
    def __init__(self, service_account_key=None, credentials=None):
        self.scopes = ['https://www.googleapis.com/auth/display-video']
        self.api_name = 'displayvideo'
        self.api_version = 'v1'
        super().__init__(self.scopes, self.api_name, self.api_version, service_account_key, credentials)