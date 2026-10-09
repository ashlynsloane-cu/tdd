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

    def test_query_rows(self):
        result = fire_gdp.get_data(
            "test/data/test_co2.csv",
            query_column="Area",
            query_value="Brazil",
        )
        expected = [
            ["Brazil", "2003", ""],
            ["Brazil", "2004", "10.0"],
            ["Brazil", "2005", "20.5"],
            ["Brazil", "2006", "30.0"],
            ["Brazil", "2007", "40.0"],
        ]
        self.assertEqual(result, expected)

    def test_return_header(self):
        result = fire_gdp.get_data(
            "test/data/test_co2.csv",
            return_header=True,
        )
        expected_header = ["Area", "Year", "Forest fires"]
        expected_rows = [
            ["Brazil", "2003", ""],
            ["Brazil", "2004", "10.0"],
            ["Brazil", "2005", "20.5"],
            ["Brazil", "2006", "30.0"],
            ["Brazil", "2007", "40.0"],
            ["Argentina", "2005", "5.0"],
        ]
        self.assertEqual(result, (expected_header, expected_rows))


class TestGetFireGDPYearData(unittest.TestCase):

    def test_matching_years(self):
        result = fire_gdp.get_fire_gdp_year_data(
            "test/data/test_co2.csv",
            "test/data/test_gdp.csv",
            "Brazil",
        )
        expected = [
            [2004, 10.0, 1000.0],
            [2005, 20.5, 2170584.50],
        ]
        self.assertEqual(result, expected)

    def test_output_types(self):
        result = fire_gdp.get_fire_gdp_year_data(
            "test/data/test_co2.csv",
            "test/data/test_gdp.csv",
            "Brazil",
        )

        self.assertIsInstance(result[0][0], int)
        self.assertIsInstance(result[0][1], float)
        self.assertIsInstance(result[0][2], float)


if __name__ == "__main__":
    unittest.main()
