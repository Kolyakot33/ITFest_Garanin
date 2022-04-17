# -*- coding: utf-8 -*-
import vk_api
import asyncio
import data_loader
import config

bot = None


def get_posts(id):  # получает посты по id
    vk_session = vk_api.VkApi(token=config.vktoken)
    _vk_api = vk_session.get_api()
    tools = vk_api.VkTools(_vk_api)
    wall = tools.get_all('wall.get', 1, {'owner_id': id})
    return wall["items"]


async def vk_poll(_bot):  # загружает посты и проверяет новости каждые refresh_period секунд
    global bot
    bot = _bot
    while True:
        print("POLL!")
        print(data_loader.get_hashtags().items())
        for _id, tag in data_loader.get_hashtags().items():
            posts = get_posts(tag["id"])
            print(tag)
            sent_posts = data_loader.get_posts()
            for post in posts:
                if not str(str(tag["id"]) + "_" + str(post["id"])) in sent_posts:
                    await process_post(post, sent_posts, tag)
        await asyncio.sleep(config.refresh_period)


async def process_post(post, sent_posts, tag):  # обрабатывает пост и отправляет пользователю
    if not tag["hashtag"].lower() in post["text"].lower():
        return
    for user in tag["subscribed"]:
        await bot.send_message(user, post["text"])
    if "attachments" in post:
        for attachment in post["attachments"]:
            if "photo" in attachment:
                for user in tag["subscribed"]:
                    try:
                        await bot.send_photo(user, attachment["photo"]["sizes"][-1]["url"])
                    except Exception:
                        pass
            elif "video" in attachment:
                for user in tag["subscribed"]:
                    try:
                        await bot.send_message(user, attachment["video"]["photo_130"])
                    except Exception:
                        pass
    if "copy_history" in post:
        await process_post(post["copy_history"][0], sent_posts, tag)

    sent_posts.append(str(tag["id"]) + "_" + str(post["id"]))
    data_loader.write_posts(sent_posts)
