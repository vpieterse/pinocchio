"""Functions for parsing and validating CSV files"""

from typing import Dict, List
import csv


class CsvStatus(object):
    """Holds information on the validity of the csv file and the returned data

    Attributes:
        valid (bool): Is the CSV file valid
        error_message (str): Error message if the CSV was not valid
        data (List[Dict[str, str]]): The extracted data from the CSV
    """

    def __init__(self,
                 valid: bool,
                 error_message: str = None,
                 data: List[Dict[str, str]] = None) -> None:
        """Create a new `CsvStatus` object

        Args:
            valid (bool): Is the CSV file valid
            error_message (str): Error message if the CSV was not valid
            data (List[Dict[str, str]]): The extracted data from the CSV
        """
        self.valid = valid
        self.error_message = error_message
        self.data = data


def validate_header(csv_file, fields: List[str]) -> CsvStatus:
    """Check if the given fields appear in the csv header

    Note:
        Calls csv_file.seek(0)

    Args:
        csv_file: The already open file to read
        fields: The list of header columns to search for

    Returns:
        A `CsvStatus` object indicating the state of the CSV file
    """
    csv_file.seek(0)
    reader = csv.reader(csv_file, fields, skipinitialspace=True)
    header: List[str] = next(reader)

    for item in fields:
        if item not in header:
            csv_file.seek(0)
            return CsvStatus(
                valid=False,
                error_message="Field " + item + " was not found "
                "in the header")

    csv_file.seek(0)
    return CsvStatus(valid=True, error_message=None)


def validate_csv(fields: List[str], file_path: str) -> CsvStatus:
    """Validate the CSV file according to the given fields

    Args:
        fields: The column headers to validate
        file_path: The path of the CSV file

    Returns:
        A 'CsvStatus' object indicating the state of the csv file
    """
    with open(file_path) as csv_file:
        header_result = validate_header(csv_file, fields)

        if not header_result.valid:
            return header_result

        reader: csv.DictReader = csv.DictReader(csv_file, skipinitialspace=True)

        # Try parsing csv into tuples according to the given fields
        items: List[Dict[str, str]] = list()

        for row in reader:
            # Make sure all fields were found in the row
            for key, value in row.items():
                if not value:
                    return CsvStatus(
                        valid=False,
                        error_message='No value found for key '
                        '\'' + key + '\' on line ' + str(reader.line_num))
            items.append(row)

    if items:
        return CsvStatus(valid=True, error_message=None, data=items)
    else:
        return CsvStatus(valid=False, error_message='No entries in CSV file')
