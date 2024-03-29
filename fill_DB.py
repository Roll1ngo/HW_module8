import json
from mongoengine.errors import NotUniqueError

from models import Author, Quote

if __name__ == '__main__':
    with open('authors.json', encoding='utf=8') as fd:
        data = json.load(fd)

        for auth in data:
            try:
                author = Author(fullname=auth.get('fullname'),
                                born_date=auth.get('born_date'),
                                born_location=auth.get('born_location'),
                                description=auth.get('description')).save()
            except NotUniqueError:
                print(f"{auth.get('fullname')} have unique field 'fullname' and already created in DataBase")

with open('quotes.json', encoding='utf=8') as fd:
    data = json.load(fd)
    for q in data:
        author, *_ = Author.objects(fullname=q.get('author'))
        quote = Quote(quote=q.get('quote'),
                      tags=q.get('tags'),
                      author=author).save()
