import tractdb
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def list_users(request):
    # Load our config file
    with open('/secrets/tractdbcouch.yml') as f:
        config = yaml.safe_load(f)

    # Create our admin object
    admin = tractdb.admin.TractDBAdmin(
        server_url=config['server_url'],
        server_admin=config['server_admin'],
        server_password=config['server_password']
    )

    return Response(repr(admin.list_users()))


def main():
    config = Configurator()
    config.add_route('list_users', '/list_users')
    config.add_view(list_users, route_name='list_users')
    app = config.make_wsgi_app()
    return app


if __name__ == '__main__':
    app = main()
    server = make_server('0.0.0.0', 8080, app)
    print('Starting up server on http://localhost:8080')
    server.serve_forever()
