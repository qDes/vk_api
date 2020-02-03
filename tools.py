import logging
import requests


def get_response(url, payload={}):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('request')
    try:
        #cafile = 'cacert.pem'  # http://curl.haxx.se/ca/cacert.pem
        response = requests.get(url, timeout=30, #verify=cafile,
                                params=payload)
        response.raise_for_status()
    except requests.Timeout:
        logger.debug(f"timeout error: {url}")
    except requests.HTTPError as err:
        code = err.response.status_code
        logger.debug(f"error url: {url}, code: {code}")
    except requests.RequestException as err:
        logger.debug(f"{err} error; url: {url}")
    else:
        return response
