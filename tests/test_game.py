import unittest

from app.game import play_mash


class TestPlayMash(unittest.TestCase):
    @staticmethod
    def get_basic_categories():
        return [
            {"name": "Food", "options": ["Mushy peas", "Chips", "Beans"]},
            {"name": "Colours", "options": ["Red", "Blue", "Green"]},
        ]

    def test_basic_mash_game(self):
        """Test the basic functionality of the MASH game with a simple set of categories."""
        result = play_mash(self.get_basic_categories(), 3)
        self.assertIsInstance(result, dict)
        self.assertIn("MASH", result)
        self.assertIn("Food", result)
        self.assertIn("Colours", result)

    def test_single_option_categories(self):
        """Test the game with categories that have only one option."""
        categories = [{"name": "Pet", "options": ["Dog"]}, {"name": "Car", "options": ["VW"]}]
        result = play_mash(categories, 2)
        self.assertEqual(result["Pet"], "Dog")
        self.assertEqual(result["Car"], "VW")

    def test_empty_categories(self):
        """No supplied categories, still returns MASH."""
        categories = []
        result = play_mash(categories, 4)
        self.assertEqual(len(result), 1)
        self.assertIn("MASH", result)

    def test_magic_number_min(self):
        """Edge case for minimum magic number."""
        result = play_mash(self.get_basic_categories(), 2)
        self.assertIn("MASH", result)
        self.assertIn("Food", result)
        with self.assertRaises(ValueError):
            play_mash(self.get_basic_categories(), 1)  # Below min

    def test_magic_number_max(self):
        """Edge case for maximum magic number."""
        result = play_mash(self.get_basic_categories(), 10)
        self.assertIn(result["Colours"], ["Red", "Blue", "Green"])
        with self.assertRaises(ValueError):
            play_mash(self.get_basic_categories(), 11)  # Below min

    def test_variable_length_categories(self):
        """Test the game with categories of varying lengths."""
        categories = [
            {"name": "Number", "options": ["One", "Two", "Three", "Four", "Five"]},
            {"name": "Letter", "options": ["A", "B", "C", "D", "E", "F", "G"]},
        ]
        result = play_mash(categories, 3)
        self.assertEqual(len(result), 3)  # MASH + 2 categories
        self.assertTrue(all(isinstance(v, str) for v in result.values()))

    def test_malformed_categories(self):
        """Test handling of malformed category data."""
        with self.assertRaises((KeyError, TypeError)):
            play_mash([{"name": "Pet"}], 3)  # Missing 'options'
        with self.assertRaises((KeyError, TypeError)):
            play_mash([{"options": ["Dog"]}], 3)  # Missing 'name'
