import pyramid.config
import pyramid.response
import pyramid.view
import tractdb.admin
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
