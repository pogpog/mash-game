import unittest

from app.llm import generate_mash_options


class TestLLM(unittest.TestCase):
    """Test the LLM functionality for generating MASH options.
    TODO: Add tests using a LLM-as-judge model to validate the generated options.
    """

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests in the class."""
        cls.theme = "Superheroes"
        cls.options = generate_mash_options(cls.theme, "huggingface")

    def test_return_type(self):
        """Test that the function actually returns a list."""
        self.assertEqual(type(self.options), list, "Expected a list of options.")

    def test_list_length(self):
        """Test that the generated list has the correct length."""
        self.assertEqual(len(self.options), 4, "Expected 4 options for the MASH game.")

    def test_options_type(self):
        """Test that all options are strings"""
        for option in self.options:
            self.assertIsInstance(option, str, "Each option should be a string.")
