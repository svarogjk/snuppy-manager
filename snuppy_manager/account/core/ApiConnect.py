import requests
from django.core.files import File
from random import randint
from os import remove
from pathlib import Path
import json

class ApiConnect:
    'Use for connect to tornado server'
    
    #server setting
    API_IP_PORT = ('127.0.0.1', ':7777')
    API_URL = '/compile/code/'
    PROTOCOL = 'http://'

    def __init__(self):
        self.status = None # 'type' in answer from tornado
        self.project_size = None # 'project_size' in asnwer from tornado
        self.path = Path() / 'temp'

    def send_compile_request(self, uuid:str, app_id:int, version:str, url:str, platform:str):
        '''
        Use this method for send request to tornado and start compile
        :param uuid: user uid (hash value)
        :param app_id: application id from database
        :param version: version name
        :param url: url to source cod on github
        :param platform: platfrom type (ios, Windows, Android)
        :return:
        '''
        full_path = (self.PROTOCOL
                     + self.API_IP_PORT[0]
                     + self.API_IP_PORT[1]
                     + self.API_URL
                     )
        params = {
            'uuid':uuid,
            'app_id':app_id,
            'version':version,
            'url':url,
            'platform':platform
        }

        self.api_request = requests.get(full_path, params=params)

        self.check_request()

        self.write_answer()

    def check_request(self):
        if not self.api_request.ok:
            raise BaseException('''
                connection problem with
                status code {}
                and message
                {}'''.format(self.api_request.status_code, self.api_request.text))

    def write_answer(self):
        js_answer = json.loads(self.api_request.text)
        if js_answer['type'] == 'success':
            self.status = 'Translated'
        else:
            # Пока известен только success, если будет другое - сразу узнаем
            raise BaseException(
                'Unpredictable behavior from tornado '
                'with type = {}'.format(js_answer['type']))

        self.project_size = str(js_answer['project_size']) # str() т.к. значение int

        self.save_file(self.project_size) # сейчас мы сохраняем только размер,
        # но в будующем это должен быть переведенный код проекта

    def save_file(self, content):
        int_name = randint(10000, 100000)  # Случайное имя в случае если будет несколько
        # запросов от разных пользователей
        self.fn = open(self.path / (str(int_name) + '.txt'), 'w+')
        self.fn.write(content)
        self.file = File(self.fn)
        self.file.name = str(int_name) + '.txt'
        # В идеале, нужно что бы формат определялся сам,
        # но пока нет разных форматов - работаем с тем txt...

    def remove_file(self):
        '''
        Use for remove temporarily created file.
        You MUST call this method when finish work with file
        :return: None
        '''
        self.fn.close()
        remove(self.fn.name)



if __name__ == '__main__':
    # :7777/compile/code/?uuid=12&app_id=234&version=1.2&url=https://github.com/kennethreitz/requests&platform=ios

    # !!!!!!Если нужны эксперименты, создайте папку temp в директории запуска
    con = ApiConnect()
    uuid = '12'
    app_id = 123
    version = '1.2'
    url = 'https://github.com/kennethreitz/requests'
    platform = 'ios'

    print(con.path, 'blalalal')
    con.send_compile_request(uuid, app_id, version, url, platform)

    print(con.project_size)


