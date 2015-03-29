from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def yo_world(request):
    return Response('Yo')


def main():
    config = Configurator()
    config.add_route('yo', '/')
    config.add_view(yo_world, route_name='yo')
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = main()
    server = make_server('0.0.0.0', 8080, app)
    print('Starting up server on http://localhost:8080')
    server.serve_forever()
