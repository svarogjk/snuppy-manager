import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options, parse_command_line

import init_db
from urls import get_url


if __name__ == '__main__':
    init_db.init_db()
    application = get_url()
    define("port", default=7777)
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")