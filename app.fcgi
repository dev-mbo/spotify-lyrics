#!/usr/bin/env python3
from flup.server.fcgi import WSGIServer
from app import create_app

if __name__ == '__main__':
    app = create_app()
    WSGIServer(app).run()