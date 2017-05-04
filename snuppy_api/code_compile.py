import json

from base_handler import BaseHandler
from compile import get_app

class CodeCompileHandler(BaseHandler):
    def get(self):
        self.common_request()

    def post(self):
        self.common_request()

    def common_request(self):
        uuid = self.get_argument('uuid')
        app_id = self.get_argument('app_id')
        version = self.get_argument('version')
        url = self.get_argument('url')
        platform = self.get_argument('platform')

        # :7777/compile/code/?uuid=12&app_id=234&version=1.2&url=https://github.com/kennethreitz/requests&platform=ios

        data = get_app(uuid=uuid, app_id=app_id, version=version, url=url, platform=platform)
        if data:
            e = json.dumps({'type': 'success', 'project_size': int(data)})
            self.write(e)

