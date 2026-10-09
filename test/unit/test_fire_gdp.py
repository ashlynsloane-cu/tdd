import unittest

from src import fire_gdp


class TestGetColumnIndex(unittest.TestCase):

    def test_name_present(self):
        header = ["Area", "Year", "Forest fires"]
        result = fire_gdp.get_column_index(header, "Forest fires")
        self.assertEqual(result, 2)

    def test_name_absent(self):
        header = ["Area", "Year", "Forest fires"]
        result = fire_gdp.get_column_index(header, "GDP")
        self.assertIsNone(result)

    def test_empty_header(self):
        result = fire_gdp.get_column_index([], "GDP")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
