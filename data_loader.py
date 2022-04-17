import ujson


def get_hashtags() -> dict:  # загружает мероприятия
    with open("hashtags.json", "r", encoding='utf-8') as f:
        hashtags = ujson.loads(f.read())
    return hashtags


def write_hashtags(users: dict):  # записывает мероприятия
    with open("hashtags.json", "w") as f:
        f.write(ujson.dumps(users))


def get_posts() -> list:  # загружает список уже отправленных постов
    with open("posts.json", "r", encoding='utf-8') as f:
        hashtags = ujson.loads(f.read())
    return hashtags


def write_posts(users: list):  # записывает отправленные посты
    with open("posts.json", "w") as f:
        f.write(ujson.dumps(users))
