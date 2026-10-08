import unittest

from dime_cli.textual_app import _parse_command


class TextualAppCommandTests(unittest.TestCase):
    def test_shortcuts_map_to_feature_commands(self):
        self.assertEqual(_parse_command("list"), ("todo", ["list"]))
        self.assertEqual(_parse_command("add write tests"), ("todo", ["add", "write", "tests"]))
        self.assertEqual(_parse_command("start"), ("focus", ["start"]))
        self.assertEqual(_parse_command("tech"), ("news", ["tech"]))


if __name__ == "__main__":
    unittest.main()