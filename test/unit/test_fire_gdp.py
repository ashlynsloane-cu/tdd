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


class TestGetData(unittest.TestCase):

    def test_get_all_rows(self):
        result = fire_gdp.get_data("test/data/test_co2.csv")
        expected = [
            ["Brazil", "2003", ""],
            ["Brazil", "2004", "10.0"],
            ["Brazil", "2005", "20.5"],
            ["Brazil", "2006", "30.0"],
            ["Brazil", "2007", "40.0"],
            ["Argentina", "2005", "5.0"],
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
