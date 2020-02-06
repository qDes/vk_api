import os
import sys
import logging

from dotenv import load_dotenv
from random import randint
from tools import download_image, fetch_xkcd_image_url, fetch_last_xkcd_number
from vk import get_wall_upload_server, save_wall_photo
from vk import upload_photo_wall, VkError


def post_random_xkcd_to_vk(access_token, group_id):
    last_comics_number = fetch_last_xkcd_number()
    xkcd_number = randint(1, last_comics_number)
    image_url = fetch_xkcd_image_url(xkcd_number)
    download_image(image_url)
    upload_server = get_wall_upload_server(access_token, group_id)
    save_wall = save_wall_photo(access_token, group_id, upload_server)
    response = upload_photo_wall(access_token, group_id, save_wall)
    post_id = response.get('response').get('post_id')
    logging.info(f"Posted {post_id}")
    os.remove("xkcd.jpg")


if __name__ == "__main__":
    logging.disable(sys.maxsize)
    load_dotenv()
    access_token = os.environ["ACCESS_TOKEN"]
    group_id = os.environ["GROUP_ID"]
    try:
        post_random_xkcd_to_vk(access_token, group_id)
    except VkError as e:
        print("Ошибка:", e)
