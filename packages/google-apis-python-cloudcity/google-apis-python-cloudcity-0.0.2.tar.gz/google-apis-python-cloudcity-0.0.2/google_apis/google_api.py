import os

from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient import discovery


class GoogleAPI:
    """
    Instantiate generic GoogleApi with the choice of using a service account or credentials file.

    Args:
        scopes (list): list of scopes https://developers.google.com/identity/protocols/oauth2/scopes
        api_name (str): the name of the API
        api_version (str): Version number
        service_account_key (str): Path to the service account key file
        credentials (str): Path to the OAUth credential file

    """

    def __init__(self, scopes, api_name, api_version, service_account_key=None, credentials=None):
        self.scopes = scopes
        self.api_name = api_name
        self.api_version = api_version
        self.get_service(service_account_key, credentials)

    def get_service(self, service_account_key=None, credentials=None):

        if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            self.service = discovery.build(f'{self.api_name}', f'{self.api_version}',
                                           cache_discovery=False)
            return

        creds = False

        if service_account_key:
            creds = self.__get_service_from_service_account(service_account_key=service_account_key)

        if credentials:
            creds = self.__get_service_from_credentials(credentials_file=credentials)

        self.service = discovery.build(f'{self.api_name}', f'{self.api_version}', credentials=creds,
                                       cache_discovery=False)
        if not creds:
            raise ValueError("No credential or Service Account Key provided.")

    def __get_service_from_service_account(self, service_account_key):
        credentials = service_account.Credentials.from_service_account_file(
            service_account_key, scopes=self.scopes)
        return credentials

    def __get_service_from_credentials(self, credentials_file):
        credentials = Credentials.from_authorized_user_file(f'{credentials_file}', self.scopes)
        if credentials is None:
            raise ValueError(
                f"The credentials in file {credentials_file} are not valid"
            )
        return credentials
