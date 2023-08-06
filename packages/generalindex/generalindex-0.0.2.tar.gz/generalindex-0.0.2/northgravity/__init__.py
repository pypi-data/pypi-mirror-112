import os
import logging; log = logging.Logger('GX SDK')

# authentication process
TOKEN = os.getenv('NG_API_AUTHTOKEN')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')

# system env variables
JOB_ID = os.environ.get('JOBID')
PIPELINE_ID = os.environ.get('PIPELINE_ID')
EID = os.environ.get('EID')
ENDPOINT = os.environ.get('NG_API_ENDPOINT', 'https://api.g-x.co')
COMPONENT_NAME = os.environ.get('NG_COMPONENT_NAME')
GROUP_NAME = os.environ.get('NG_STATUS_GROUP_NAME')

# Check if the LOGIN is properly set
if TOKEN in [None, '']:
    # if not Token, it's a local run - LOGIN & PASSWORD must be provided
    if LOGIN in [None, '']:
        raise Exception("No LOGIN found. Set the environment variable with the LOGIN used to connect to the application")
    if PASSWORD in [None, '']:
        raise Exception("No PASSWORD found. Set the environment variable with the PASSWORD used to connect to the application")


from .DatalakeHandler import *
from .TaskHandler import *
from .StatusHandler import *
from .Timeseries import *