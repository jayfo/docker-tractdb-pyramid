import pyramid.config
import pyramid.response
import pyramid.view
import wsgiref.simple_server


@pyramid.view.view_config(route_name='echo', renderer='json')
def echo(request):
    return request.json_body


def main():
    config = pyramid.config.Configurator()
    config.scan('views')

    config.add_route('accounts', '/accounts')
    config.add_route('account', '/accounts/{account}')

    config.add_route('couch', '/couch{request:.*}')

    config.add_route('echo', '/echo')
    config.add_route('yo', '/yo')

    app = config.make_wsgi_app()

    return app


if __name__ == '__main__':
    app = main()

    print('Starting up server on http://localhost:8080')
    server = wsgiref.simple_server.make_server('0.0.0.0', 8080, app)
    server.serve_forever()
