import pyramid.config
import pyramid.response
import pyramid.view
import tractdb.admin
import wsgiref.simple_server
import yaml


@pyramid.view.view_defaults(route_name='account', renderer='json')
class AccountView:
    def __init__(self, request):
        self.request = request

    @pyramid.view.view_config(route_name='accounts', request_method='GET')
    def get_all(self):
        """ Get a list of accounts.
        """
        # Get the accounts
        admin = self._get_admin()
        list_accounts = admin.list_accounts()

        # Return appropriately
        self.request.response.status_int = 200
        return list_accounts

    # @pyramid.view.view_config(request_method='GET')
    # def get(self):
    #     pass

    @pyramid.view.view_config(route_name='accounts', request_method='POST')
    def post(self):
        """ Create an account.
        """

        # Our JSON parameter, this could be validated
        json = self.request.json_body
        account = json['account']
        account_password = json['password']

        # Our admin object
        admin = self._get_admin()

        # Check if the account exists
        if account in admin.list_accounts():
            self.request.response.status_int = 409
            return

        # Create the account
        admin.create_account(account, account_password)

        # Return appropriately
        self.request.response.status_int = 201

    # @pyramid.view.view_config(request_method='PUT')
    # def put(self):
    #     pass

    @pyramid.view.view_config(request_method='DELETE')
    def delete(self):
        """ Delete an account.
        """

        # Our account parameter
        account = self.request.matchdict['account']

        # Our admin object
        admin = self._get_admin()

        # Check if the account exists
        if account not in admin.list_accounts():
            self.request.response.status_int = 404
            return

        # Delete the account
        admin.delete_account(account)

        # Return appropriately
        self.request.response.status_int = 200

    @staticmethod
    def _get_admin():
        # Load our config file
        with open('/secrets/tractdbcouch.yml') as f:
            config = yaml.safe_load(f)

        # Create our admin object
        admin = tractdb.admin.TractDBAdmin(
            server_url=config['server_url'],
            server_admin=config['server_admin'],
            server_password=config['server_password']
        )

        return admin


@pyramid.view.view_defaults(route_name='couch', renderer='json')
class CouchView:
    def __init__(self, request):
        self.request = request

    @pyramid.view.view_config(request_method='GET')
    def get(self):
        return self.request.matchdict['request']


@pyramid.view.view_config(route_name='echo', renderer='json')
def echo(request):
    return request.json_body


@pyramid.view.view_config(route_name='yo', renderer='json')
def yo(request):
    return 'yo'


def main():
    config = pyramid.config.Configurator()
    config.scan()

    config.add_route('accounts', '/accounts')
    config.add_route('account', '/accounts/{account}')

    config.add_route('couch', '/couch/{request}')

    config.add_route('echo', '/echo')
    config.add_route('yo', '/yo')

    app = config.make_wsgi_app()

    return app


if __name__ == '__main__':
    app = main()

    print('Starting up server on http://localhost:8080')
    server = wsgiref.simple_server.make_server('0.0.0.0', 8080, app)
    server.serve_forever()
