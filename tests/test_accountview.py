import requests
import unittest


class TestAccountView(unittest.TestCase):
    ACCOUNTS_URL = 'https://tractdb.org/api/accounts'

    TEST_ACCOUNT = 'tractdb_pyramid_testaccountview_test_account'
    TEST_ACCOUNT_PASSWORD = 'tractdb_pyramid_testaccountview_test_account_password'

    def test_create_and_delete_account(self):
        # Ensure it does not already exist
        r = requests.delete(
            '{}/{}'.format(
                TestAccountView.ACCOUNTS_URL,
                TestAccountView.TEST_ACCOUNT
            )
        )

        # Create the account
        r = requests.post(
            TestAccountView.ACCOUNTS_URL,
            json={
                'account': TestAccountView.TEST_ACCOUNT,
                'password': TestAccountView.TEST_ACCOUNT_PASSWORD
            }
        )
        self.assertEqual(r.status_code, 201)

        # Test the creating it again fails
        r = requests.post(
            TestAccountView.ACCOUNTS_URL,
            json={
                'account': TestAccountView.TEST_ACCOUNT,
                'password': TestAccountView.TEST_ACCOUNT_PASSWORD
            }
        )
        self.assertEqual(r.status_code, 409)

        # Test the account exists
        r = requests.get(
            TestAccountView.ACCOUNTS_URL,
        )
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
        self.assertIn(TestAccountView.TEST_ACCOUNT, r.json())

        # Delete the account
        r = requests.delete(
            '{}/{}'.format(
                TestAccountView.ACCOUNTS_URL,
                TestAccountView.TEST_ACCOUNT
            )
        )
        self.assertEqual(r.status_code, 200)

        # Test that deleting the account again fails
        r = requests.delete(
            '{}/{}'.format(
                TestAccountView.ACCOUNTS_URL,
                TestAccountView.TEST_ACCOUNT
            )
        )
        self.assertEqual(r.status_code, 404)

        # Test the account is gone
        r = requests.get(
            TestAccountView.ACCOUNTS_URL,
        )
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
        self.assertNotIn(TestAccountView.TEST_ACCOUNT, r.json())

