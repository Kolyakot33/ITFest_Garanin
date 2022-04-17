import ujson


def get_hashtags() -> dict:  # загружаем мероприятия
    with open("hashtags.json", "r", encoding='utf-8') as f:
        hashtags = ujson.loads(f.read())
    return hashtags


def write_hashtags(users: dict):  # записываем мероприятия
    with open("hashtags.json", "w", encoding='utf-8') as f:
        f.write(ujson.dumps(users))


def get_posts() -> list:  # загружаем список уже отправленных постов
    with open("posts.json", "r", encoding='utf-8') as f:
        hashtags = ujson.loads(f.read())
    return hashtags


def write_posts(users: list):  # записываем отправленные посты
    with open("posts.json", "w", encoding='utf-8') as f:
        f.write(ujson.dumps(users))
