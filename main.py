import redis
from redis_lru import RedisLRU
from mongoengine import connect

from models import Author, Quote, connect

client = redis.Redis(host='localhost', port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_quotes_by_teg(tag: str) -> list[str]:
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result

def find_quotes_by_some_tags(tag: str) -> list[str]:
    tags_list = tag.strip().split(',')
    quotes = Quote.objects(tags__in=tags_list)
    return [q.quote for q in quotes]

@cache
def find_quotes_by_author(author_name: str) -> str:
    authors = Author.objects(fullname__iregex=author_name).all()
    for author in authors:
        if author:
            quotes = Quote.objects(author=author.id)
            for q in quotes:
                return f'{q.quote}, \u00A9 {author.fullname}'
        else:
            return f'No author found with request {author_name}'


COMMANDS = {
    ('name', 'author'): find_quotes_by_author,
    ('tag',): find_quotes_by_teg,
    ('tags',): find_quotes_by_some_tags
}


def parser(text: str) -> tuple[callable, str] or str:
    text = text.strip().split(':')
    for comm, func in COMMANDS.items():
        if text[0].lower() in comm:
            text = text[1:]
            for t in text:
                return func, t
    return "Wrong command"


def main():
    while True:
        user_input = input("input_require >>>")
        if user_input == 'exit':
            print('Bye')
            break
        command, data = parser(user_input)
        print(command(data))


if __name__ == '__main__':
    main()
