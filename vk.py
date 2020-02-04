import os
import requests

from dotenv import load_dotenv
from tools import get_response


def download_image(image_url):
    image = get_response(image_url).content
    with open('xkcd.jpg', "wb") as f:
        f.write(image)


def fetch_xkcd_image():
    url = "https://xkcd.com/353/info.0.json"
    xkcd = get_response(url).json()
    img_url = xkcd.get('img')
    comment = xkcd.get('alt')
    print(comment)
    if img_url:
        download_image(img_url)


def get_wall_upload_server(token, group_id):
    # https://vk.com/dev/photos.getWallUploadServer
    url = "https://api.vk.com/method/photos.getWallUploadServer?"
    payload = {"group_id": group_id,
            "access_token": access_token,
            'v': 5.103}
    upload_server = get_response(url, payload).json().get('response')
    upload_url = upload_server.get('upload_url')
    with open('xkcd.jpg', 'rb') as file:
        url = upload_url
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
    return response.json()


def save_wall_photo(token, group_id, upload_server):
    # https://vk.com/dev/photos.saveWallPhoto
    server = upload_server.get('server')
    photo = upload_server.get('photo')
    hash_ = upload_server.get('hash')
    url = "https://api.vk.com/method/photos.saveWallPhoto?"
    payload = {"access_token": token,
            "group_id": group_id,
            "photo": photo,
            "hash": hash_,
            "server": server,
            'v': 5.103
            }
    response = get_response(url, payload).json().get('response')
    if response:
        return response[0]
    return None
    

def upload_photo_wall(token, group_id, save_wall):
    # https://vk.com/dev/wall.post
    owner_id = save_wall.get('owner_id')
    photo_id = save_wall.get('id')
    wall_post_url =  "https://api.vk.com/method/wall.post?"
    pay_load = {"owner_id": f"-{group_id}",
            "from_group": 1,
            "access_token": token,
            "attachments": f"photo{owner_id}_{photo_id}",
            'v': 5.103}
    url = "https://api.vk.com/method/photos.saveWallPhoto?"
    response = get_response(wall_post_url, pay_load)
    return response.json()


if __name__ == "__main__":
    load_dotenv()
    access_token = os.environ["ACCESS_TOKEN"]
    group_id = os.environ["GROUP_ID"]
    upload_server = get_wall_upload_server(access_token, group_id)
    print(upload_server)
    save_wall = save_wall_photo(access_token, group_id, upload_server)
    print(save_wall)
    response = upload_photo_wall(access_token, group_id, save_wall)
    print(response)
