import unittest
from unittest.mock import patch

from dime_cli.main import main


class MainEntryPointTests(unittest.TestCase):
    def test_no_args_launches_textual_app(self):
        with patch("dime_cli.main.run_textual_app") as run_textual_app:
            main([])

        run_textual_app.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()