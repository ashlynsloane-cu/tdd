import csv


def get_data(file_name,
             query_column=None,
             query_value=None,
             return_header=False):
    rows = []

    with open(file_name, newline="") as file:
        reader = csv.reader(file)
        header = next(reader)

        if query_column is not None and query_value is not None:
            query_index = get_column_index(header, query_column)

            for row in reader:
                if row[query_index] == query_value:
                    rows.append(row)
        else:
            for row in reader:
                rows.append(row)

    if return_header:
        return header, rows

    return rows


def get_column_index(header, column_name):
    try:
        return header.index(column_name)
    except ValueError:
        return None


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    pass
