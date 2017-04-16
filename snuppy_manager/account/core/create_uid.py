from hashlib import md5
from datetime import datetime


def create_uid(id:int, name:str, created_date:datetime) -> str:

    try:
        date = str(created_date)
        id_str = str(id)
        hash = md5((date + id_str + name).encode('utf-8')).hexdigest()
    except TypeError:
        raise TypeError('Wrong type arguments!')
    return hash

if __name__ == '__main__':
    date = datetime.now()
    uid = create_uid(123, 'Sasha', date)
    print(uid)