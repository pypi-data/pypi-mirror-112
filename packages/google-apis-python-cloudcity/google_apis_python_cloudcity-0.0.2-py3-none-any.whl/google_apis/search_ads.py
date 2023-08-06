from google_apis.google_api import GoogleAPI


class SearchAds(GoogleAPI):
    """
    This class is to instanciate the Search Ads 360 API
    https://developers.google.com/search-ads/v2/reference

    """

    def __init__(self, service_account_key=None, credentials=None, scopes=None):
        self.scopes = scopes if scopes else ['https://www.googleapis.com/auth/doubleclicksearch']
        self.api_name = 'doubleclicksearch'
        self.api_version = 'v2'
        super().__init__(self.scopes, self.api_name, self.api_version, service_account_key, credentials)
