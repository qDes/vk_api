import logging
import requests


def get_response(url, payload={}):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('request')
    try:
        response = requests.get(url, timeout=30,
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


def download_image(image_url, image_path="xkcd.jpg"):
    image = get_response(image_url).content
    with open(image_path, "wb") as f:
        f.write(image)


def fetch_xkcd_image_url(num):
    url = f"https://xkcd.com/{num}/info.0.json"
    response = get_response(url)
    xkcd = response.json()
    image_url = xkcd.get("img")
    return image_url


def fetch_last_xkcd_number():
    url = "https://xkcd.com/info.0.json"
    response = get_response(url).json()
    last_num = response.get("num")
    return last_num
