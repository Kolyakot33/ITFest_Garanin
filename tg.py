import aiogram
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, Message, \
    CallbackQuery

import data_loader
from config import token



bot = aiogram.Bot(token=token)
dispatcher = aiogram.Dispatcher(bot)


def get_subscribe_menu(id):  # генерирует меню подписки/отписки
    menu = InlineKeyboardMarkup()
    for _id, tag in data_loader.get_hashtags().items():
        symbol = "✅" if id in tag["subscribed"] else "❌"
        menu.add(InlineKeyboardButton(text=f'{symbol} {tag["hashtag"]} - {tag["description"]}',
                                                    callback_data="toggle " + _id))
    return menu


main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
b_subscribe_menu = KeyboardButton("Подписаться на новости")
b_support = KeyboardButton("Обратная связь")
main_kb.add(b_subscribe_menu)
main_kb.add(b_support)

# команды

@dispatcher.message_handler(commands=["help"])
async def _help(message: Message):
    await message.reply("Вот список доступных команд:\n"
                        "/subscribe <id>- подписаться на новости/отписаться от новостей\n"
                        "/support - обратная связь\n"
                        "/s - кнопки для подписки/отписки")


@dispatcher.message_handler(lambda s: s.text in ["/support", "/feedback", "Обратная связь"])
async def _support(message: Message):
    await message.reply("Привет! Если у вас возникли какие-либо вопросы, то вот наши контакты: \n"
                        "Группа ВКонтакте Научим.online https://vk.com/nauchim.online\n"
                        "Сайт с мероприятиями https://www.научим.online")


@dispatcher.message_handler(commands=["start"])
async def _start(message: Message):
    await message.reply("Привет! Этот бот позволяет получать новости мероприятий. Используйте кнопки ниже для навигации или напишите /help для просмотра списка команд.",
                        reply_markup=main_kb)


@dispatcher.message_handler(commands=["list"])
async def _list(message: Message):
    text=""
    for _id, tag in data_loader.get_hashtags().items():  # добавляем каждое мероприятие
        print(tag["description"])
        text+= str(_id) +". " + tag["description"] + " - " + "https://vk.com/" + (str(tag["id"]) if not str(tag["id"]).startswith("-") else "club" + str(tag["id"])[1::]) + "\n"
    await message.reply(f"Список всех мероприятий\n" + text)



@dispatcher.message_handler(lambda s: s.text in ["/s", "Подписаться на новости"])
async def _subscribe_menu(message: Message):
    await message.reply("Список доступных мероприятий:\n ✅ - вы подписаны \n ❌ - вы не подписаны", reply_markup=get_subscribe_menu(message.from_user.id))



@dispatcher.message_handler(commands=["subscribe"])
async def subscribe(message: Message):
    _id = message.text.split()[1]
    tags = data_loader.get_hashtags()
    tags[_id]["subscribed"].append(message.chat.id)
    data_loader.write_hashtags(tags)



@dispatcher.callback_query_handler(lambda s: s.data.startswith("toggle"))
async def _toggle_subscribe(call: CallbackQuery):  # подписывает/отписывает пользователя от мероприятия
    _id = call.data.split()[1]
    tags = data_loader.get_hashtags()
    if call.from_user.id in tags[_id]["subscribed"]:
        tags[_id]["subscribed"].remove(call.from_user.id)
    else:
        tags[_id]["subscribed"].append(call.from_user.id)
    data_loader.write_hashtags(tags)
    await call.answer("Успех!")
    await call.message.edit_reply_markup(reply_markup=get_subscribe_menu(call.from_user.id))

#################################################################################


async def send_message(**kwargs):
    await bot.send_message(**kwargs)


async def send_photo(**kwargs):
    await bot.send_photo(**kwargs)
