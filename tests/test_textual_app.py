import unittest

from dime_cli.tui.commands import parse_command


class TextualAppCommandTests(unittest.TestCase):
    def test_shortcuts_map_to_feature_commands(self):
        self.assertEqual(parse_command("list"), ("todo", ["list"]))
        self.assertEqual(parse_command("add write tests"), ("todo", ["add", "write", "tests"]))
        self.assertEqual(parse_command("start"), ("focus", ["start"]))
        self.assertEqual(parse_command("tech"), ("news", ["tech"]))


if __name__ == "__main__":
    unittest.main()