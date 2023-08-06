import base64
from . import *
import logging, sys

# Create the logger for the SDK
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.Logger('GX SDK')



class Authenticator:
    def __init__(self):
        self.token = TOKEN
        self.login = LOGIN
        self.password = PASSWORD

    def get_token(self):
        if self.token is not None:
            log.debug('Authentication with Web Token ...')
            return {'Authorization': f'Bearer {self.token}'}

        else:
            if self.login is not None and self.password is not None:
                log.debug('Authentication with Credentials ...')
                credentials = self.login + ":" + self.password
                message_bytes = credentials.encode('ascii')
                base64_enc = base64.b64encode(message_bytes).decode('UTF-8')

                d = {'Authorization': f"Basic {base64_enc}"}
                return d

            else:
                log.error('No login or password provided, neither token can be read form environment variable.')
                raise Exception('Authentication issue : no credentials found')
