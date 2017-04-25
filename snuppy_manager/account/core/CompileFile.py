import requests
from django.core.files import File
from random import randint
from os import remove
from pathlib import Path


class CompileFile:

    def __init__(self, url):
        url_content = self.download_file(url)
        self.path = Path() / 'temp'
        self.save_file(url_content)


    def download_file(self, url):
        return requests.get(url).content

    def save_file(self, url_content):
        int_name = randint(10000, 100000) #Случайное имя в случае если будет несколько
        # запросов от разных пользователей
        self.fn = open(self.path / str(int_name), 'w+b')
        self.fn.write(url_content)
        self.file = File(self.fn)
        self.file.name = str(int_name)

    def remove_file(self):
        self.fn.close()
        remove(self.fn.name)

if __name__ == '__main__':
    url = 'https://github.com/kennethreitz/requests'
    c = CompileFile(url)
    print(c.file)
    print(dir(c.file))
    print(c.file.name)
    c.remove_file()
