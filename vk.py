import requests

from tools import get_response


class VkError(Exception):
    pass


def get_wall_upload_server(token, group_id):
    # https://vk.com/dev/photos.getWallUploadServer
    url = "https://api.vk.com/method/photos.getWallUploadServer?"
    payload = {"group_id": group_id, "access_token": token, "v": 5.103}
    upload_server = get_response(url, payload).json()
    if upload_server.get("error"):
        error_msg = upload_server.get("error").get("error_msg")
        raise VkError(error_msg)
    upload_server = upload_server.get("response")
    upload_url = upload_server.get("upload_url")
    with open("xkcd.jpg", "rb") as file:
        url = upload_url
        files = {
            "photo": file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
    return response.json()


def save_wall_photo(token, group_id, upload_server):
    # https://vk.com/dev/photos.saveWallPhoto
    server = upload_server.get("server")
    photo = upload_server.get("photo")
    hash_ = upload_server.get("hash")
    url = "https://api.vk.com/method/photos.saveWallPhoto?"
    payload = {
        "access_token": token,
        "group_id": group_id,
        "photo": photo,
        "hash": hash_,
        "server": server,
        "v": 5.103,
    }
    response = requests.post(url, payload)
    response.raise_for_status()
    response = response.json()
    if response.get("error"):
        error_msg = response.get("error").get("error_msg")
        raise VkError(error_msg)
    return response.get("response")[0]


def upload_photo_wall(token, group_id, save_wall):
    # https://vk.com/dev/wall.post
    owner_id = save_wall.get("owner_id")
    photo_id = save_wall.get("id")
    wall_post_url = "https://api.vk.com/method/wall.post?"
    pay_load = {
        "owner_id": f"-{group_id}",
        "from_group": 1,
        "access_token": token,
        "attachments": f"photo{owner_id}_{photo_id}",
        "v": 5.103,
    }
    response = get_response(wall_post_url, pay_load).json()
    if response.get("error"):
        error_msg = response.get("error").get("error_msg")
        raise VkError(error_msg)

    return response
