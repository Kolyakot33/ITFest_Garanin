# -*- coding: utf-8 -*-
import vk_api
import asyncio
import data_loader
import config
from tg import send_photo, send_message


def get_posts(id): #получает посты по id
    vk_session = vk_api.VkApi(config.vktoken)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    tools = vk_api.VkTools(vk_session)
    wall = tools.get_all('wall.get', 10, {'owner_id': id})
    return wall["items"]


async def vk_poll(): # загружает посты и проверяет новости каждые refresh_period секунд
    while True:
        print("POLL!")
        for tag in data_loader.get_hashtags().values():
            posts = get_posts(tag["id"])
            print(posts)
            sent_posts = data_loader.get_posts()
            for post in posts:
                if not str(str(tag["id"]) + "_" + str(post["id"])) in sent_posts:
                    await process_post(post, sent_posts, tag)
        await asyncio.sleep(config.refresh_period)


async def process_post(post, sent_posts, tag): # обрабатывает пост и отправляет пользователю
    print(post)
    if not tag["hashtag"].lower() in post["text"].lower():
        return
    for user in tag["subscribed"]:
        await send_message(user, post["text"])
    if "attachments" in post:
        for attachment in post["attachments"]:
            if "photo" in attachment:
                for user in tag["subscribed"]:
                    try:
                        await send_photo(user, attachment["photo"]["sizes"][-1]["url"])
                    except Exception:
                        pass
            elif "video" in attachment:
                for user in tag["subscribed"]:
                    try:
                        await send_message(user, attachment["video"]["photo_130"])
                    except Exception:
                        pass
    if "copy_history" in post:
        await process_post(post["copy_history"][0], sent_posts, tag)

    sent_posts.append(str(tag["id"]) + "_" + str(post["id"]))
    data_loader.write_posts(sent_posts)
