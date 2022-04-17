# -*- coding: utf-8 -*-

import asyncio
from tg import dispatcher
from vk import vk_poll

# запуск
ioloop = asyncio.get_event_loop()
tasks = [
    ioloop.create_task(vk_poll()),  # проверка записей
    ioloop.create_task(dispatcher.start_polling())  # telegram бот
]
ioloop.run_until_complete(asyncio.wait(tasks))
ioloop.close()
