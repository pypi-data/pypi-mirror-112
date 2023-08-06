import os
import logging

logging.basicConfig(format="[%(levelname)s]: %(message)s", level=os.environ.get('CL_LOG_LEVEL', 20))

def format_url(path):
    if os.environ.get('DEBUG'):
        return 'http://localhost:{}/v1/'.format(os.environ.get('DEBUG_PORT')) + path
    else:
        return 'https://{}/api/v1/' + path
