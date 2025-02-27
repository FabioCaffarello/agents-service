import unittest

from cliargs.cli import new_args_parser


class TestCli(unittest.TestCase):
    def test_new_args_parser(self):
        parser = new_args_parser("Test description")
        self.assertEqual(parser.description, "Test description")


if __name__ == "__main__":
    unittest.main()
