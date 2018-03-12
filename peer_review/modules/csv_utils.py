"""Functions for parsing and validating CSV files"""

from typing import Dict, List
import logging
import csv

logger = logging.getLogger(__name__)

class OptionalKeyNotFoundError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


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

    try:
        header: List[str] = next(reader)
    except UnicodeDecodeError as e:
        logger.error('Failed to decode byte as utf-8 in CSV file', exc_info=1)
        return CsvStatus(valid=False, error_message=str(e))

    for item in fields:
        if item not in header:
            csv_file.seek(0)
            return CsvStatus(
                valid=False,
                error_message="Field " + item + " was not found "
                "in the header")

    csv_file.seek(0)
    return CsvStatus(valid=True, error_message=None)


def contains_duplicates(items: List[Dict[str, str]], primary_key_field: str) -> CsvStatus:
    """Check if duplicate primary keys were found in the Csv file

    Args:
        items: The list of item dicts to check
        primary_key_field: The header in the CSV to check for duplicates

    Returns:
        Only returns subsequent duplicates in data.

        A CsvStatus object that has the following cases:

        No duplicates found:
            valid = True
            data = None

        Duplicates found:
            valid = False
            data != None

        Primary key not found:
            Valid = False
            data = None
    """
    duplicates: List[Dict[str, str]] = list()
    found_primary_keys: Dict[str, bool] = dict()

    for item in items:
        if primary_key_field not in item:
            return CsvStatus(valid=False,
                             error_message='Primary key field %s was not '
                                           'found in one of the rows' %
                                           primary_key_field,
                             data=None);

        if not item[primary_key_field] in found_primary_keys:
            found_primary_keys[item[primary_key_field]] = True
        else:
            duplicates.append(item)

    if duplicates:
        return CsvStatus(valid=False,
                         error_message='CSV file contains duplicate primary keys.',
                         data=duplicates)
    else:
        return CsvStatus(valid=True, data=None)


def validate_optionals(fields: List[str], optional_fields: List[str]) -> None:
    """Check that all optionals are in fields, otherwise raise exception

    Args:
        fields: All the column titles in the CSV
        optionals: The fields in the headers that can be empty

    Raises:
        OptionalKeyNotFoundError: when a key in the optional was not found
            in fields

    Returns:
        None
    """

    for val in optional_fields:
        if val not in fields:
            raise OptionalKeyNotFoundError('Optional key "{0}" was not found in the fields list'.format(val))


def validate_csv(fields: List[str], file_path: str,
                 primary_key_field: str = None,
                 optional_fields: List[str] = None) -> CsvStatus:
    """Try to parse the csv file and return the status and optionally the data

    Note:
        This is the entry point for validating a csv

    Args:
        fields: The column headers to validate
        file_path: The path of the CSV file
        optional_fields: Fields in the fields array that can be empty
        primary_key_field: The header column to use as primary key for checking
            duplicates

    Returns:
        A 'CsvStatus' object indicating the state of the csv file
        and the data if it was valid

    Note:
        Prints an exception message when there is a UnicodeDecodeError
        and the data if it was valid.

        If a key was marked as optional, when it was not in the CSV
        its value will be ''
    """
    if optional_fields:
        validate_optionals(fields, optional_fields)

    with open(file_path) as csv_file:
        header_result = validate_header(csv_file, fields)

        if not header_result.valid:
            return header_result

        reader: csv.DictReader = csv.DictReader(csv_file, skipinitialspace=True)

        # Try parsing csv into tuples according to the given fields
        items: List[Dict[str, str]] = list()

        try:
            for row in reader:
                # Make sure all fields were found in the row
                for key, value in row.items():
                    if not value:
                        return CsvStatus(
                            valid=False,
                            error_message='No value found for key '
                            '\'' + key + '\' on line ' + str(reader.line_num))
                items.append(row)
        except UnicodeDecodeError:
            logger.error('Failed to decode byte as utf-8 in CSV file at line {0}'.format(reader.line_num),
                         exc_info=1)
            return CsvStatus(valid=False,
                             error_message='Invalid byte at line {0}: Cannot decode as utf-8'.format(reader.line_num))
        for row in reader:
            # Make sure all fields were found in the row
            for key, value in row.items():
                if not value:
                    if optional_fields and key not in optional_fields or not optional_fields:
                        return CsvStatus(
                                valid=False,
                                error_message='No value found for key '
                                              '\'' + key + '\' on line '
                                              + str(
                                                reader.line_num))

            items.append(row)

        if primary_key_field:
            duplicate_result: CsvStatus = contains_duplicates(items=items, primary_key_field=primary_key_field)

            if not duplicate_result.valid and duplicate_result.data:
                return duplicate_result

    if items:
        return CsvStatus(valid=True, error_message=None, data=items)
    else:
        return CsvStatus(valid=False, error_message='No entries in CSV file')
