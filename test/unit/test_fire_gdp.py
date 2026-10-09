import unittest

from src import fire_gdp


class TestGetColumnIndex(unittest.TestCase):

    def test_name_present(self):
        header = ["Area", "Year", "Forest fires"]
        result = fire_gdp.get_column_index(header, "Forest fires")
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
