from os.path import isfile

from db import db
from db_path import SQLITE_FILE_PATH
import models


def init_db():
    if not isfile(SQLITE_FILE_PATH):
        print('[ init DB ]')
        create_db()

def create_db():
    db.generate_db(models.Base)


if __name__ == '__main__':
    init_db()