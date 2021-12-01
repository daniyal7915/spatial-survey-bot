from unittest import TestCase, main
from engine.utils.utils import credentials
from tests.utils.data import Data, Result


class CredentialsTest(TestCase, Data, Result):
    def test_credentials(self):
        """Test the credentials function"""
        self.assertEqual(credentials(self.data_credentials), self.result_credentials)


if __name__ == "__main__":
    main()
