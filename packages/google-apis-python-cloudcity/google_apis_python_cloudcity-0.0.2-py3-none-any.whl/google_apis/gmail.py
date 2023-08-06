from google_apis.google_api import GoogleAPI

class GMail(GoogleAPI):
    """
    This class is to instanciate the GMail manager API
    https://developers.google.com/gmail/api/reference/rest
    """

    def __init__(self, service_account_key=None, credentials=None):
        self.scopes = []
        self.api_name = 'gmail'
        self.api_version = 'v1'
        super().__init__(self.scopes, self.api_name, self.api_version, service_account_key, credentials)



    def create_message(self, to: str, subject: str, message_text: str) -> dict:
        """Create a message for an email.

        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.

        Returns:
          An object containing a base64url encoded email object.
        """

        from email.mime.text import MIMEText
        import base64
        message = MIMEText(message_text, 'html', _charset='utf-8')
        # message['sender'] = "no-reply@dqna.com"
        message['to'] = to
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
        return {
            'raw': raw_message.decode("utf-8")
        }

    def send_message(self, message) -> str:
        """Send an email message.

        Args:
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.

        Returns:
          Sent Message.
        """

        from urllib3.exceptions import HTTPError
        try:
            message = (self.service.users().messages().send(userId="me", body=message)
                       .execute())
            print(f'Message Id:{message["id"]}')
            return message
        except HTTPError as error:
            print('An error occurred: %s' % error)
            return ""
