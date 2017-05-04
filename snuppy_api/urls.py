import tornado.web

from code_compile import CodeCompileHandler


def get_url():
    app = tornado.web.Application(
        [
            (r"/compile/code/", CodeCompileHandler),
        ],
        autoreload=True,
    )
    return app