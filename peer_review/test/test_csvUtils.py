from django.test import TestCase
import peer_review.modules.csv_utils as csv_utils
import os
import logging
from peer_review.modules.csv_utils import OptionalKeyNotFoundError
from typing import Dict


class CsvUtilsTest(TestCase):
    """Tests relating to the csvUtils module

    Note:
        Only the existence of error_message is tested


    TODO(egeldenhuys): Test styles independently
    TODO(egeldenhuys): Test if `headers` not in `fields` are ignored
    TODO(egeldenhuys): Test duplicate user ids
    """

    def setUp(self):
        module_dir = os.path.dirname(__file__)
        self.csv_dir: str = module_dir + "/test_csvUtils"
        self.fields: list = [
            'title', 'initials', 'name', 'surname', 'cell', 'email', 'user_id'
        ]

    def test_header_validation(self):
        # Pass when all fields are also in the csv header
        # Pass when there are spaces after the ',' delimiter
        result: csv_utils.CsvStatus = csv_utils.validate_csv(
                self.fields, self.csv_dir + '/valid.csv')
        self.assertEqual(result.valid, True,
                         "Could not find all the fields in csv header")

        # Fail when field not found in csv header
        result = csv_utils.validate_csv(self.fields,
                                        self.csv_dir + '/invalid_header.csv')
        self.assertEqual(result.valid, False)
        self.assertEqual(result.data, None)
        self.assertNotEqual(result.error_message, None)

        # Pass when there are extra fields in the csv header
        result = csv_utils.validate_csv(
                self.fields, self.csv_dir + '/valid_header_extra.csv')
        self.assertEqual(result.valid, True)

    def test_user_validation(self):
        result: csv_utils.CsvStatus = csv_utils.validate_csv(
                self.fields, self.csv_dir + '/valid_users.csv')
        self.assertEqual(result.valid, True)
        self.assertNotEqual(result.data, None)
        self.assertEqual(len(result.data), 3)

        user1: Dict[str, str] = dict()
        user1['title'] = 'Mrs'
        user1['initials'] = 'T'
        user1['name'] = 'Tina'
        user1['surname'] = 'Smith'
        user1['email'] = 'Tsmith@example.com'
        user1['cell'] = '323424'
        user1['user_id'] = 'u478955545'

        user2: Dict[str, str] = dict()
        user2['title'] = 'Mr'
        user2['initials'] = 'J'
        user2['name'] = 'John'
        user2['surname'] = 'Doe'
        user2['email'] = 'john.doe@example.com'
        user2['cell'] = '838374742'
        user2['user_id'] = 'johny'

        user3: Dict[str, str] = dict()
        user3['title'] = 'Mr'
        user3['initials'] = 'F'
        user3['name'] = 'Fred'
        user3['surname'] = 'Smith'
        user3['email'] = 'fred.smith@example.com'
        user3['cell'] = '333343'
        user3['user_id'] = 'TheFred'

        # Pass when users are returned in order according to the structure
        # List[Dict[str, str]]
        self.assertDictEqual(result.data[0], user2)
        self.assertDictEqual(result.data[1], user3)
        self.assertDictEqual(result.data[2], user1)

    def test_no_users(self):
        result: csv_utils.CsvStatus = csv_utils.validate_csv(
                self.fields, self.csv_dir + '/no_users.csv')
        self.assertEqual(result.valid, False)
        self.assertNotEqual(result.error_message, None)
        self.assertEqual(result.data, None)

    def test_invalid_row(self):
        result: csv_utils.CsvStatus = csv_utils.validate_csv(
                self.fields, self.csv_dir + '/invalid_row.csv')
        self.assertEqual(result.valid, False)
        self.assertNotEqual(result.error_message, None)
        self.assertEqual(result.data, None)

        result = csv_utils.validate_csv(self.fields,
                                        self.csv_dir + '/invalid_row2.csv')
        self.assertEqual(result.valid, False)
        self.assertNotEqual(result.error_message, None)
        self.assertEqual(result.data, None)

    def test_styles(self):
        result: csv_utils.CsvStatus = csv_utils.validate_csv(
                self.fields, self.csv_dir + '/valid_style.csv')
        self.assertEqual(result.valid, True)

        user2: Dict[str, str] = dict()
        user2['title'] = 'Mr'
        user2['initials'] = 'J'
        user2['name'] = 'John Fred James'
        user2['surname'] = 'Doe'
        user2['email'] = 'john.doe@example.com'
        user2['cell'] = '838374742'
        user2['user_id'] = 'johny'

        self.assertDictEqual(result.data[0], user2)

    def test_primary_key(self):
        result: csv_utils.CsvStatus = csv_utils.validate_csv(
                ['user_id', 'name'], self.csv_dir + '/invalid_duplicate_pk.csv',
                primary_key_field='user_id')
        self.assertEqual(result.valid, False)
        self.assertNotEqual(result.error_message, '')
        self.assertNotEqual(result.error_message, None)
        self.assertNotEqual(result.data, None)

        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0]['user_id'], 'fred')
        self.assertEqual(result.data[0]['name'], 'The Fred')

        result: csv_utils.CsvStatus = csv_utils.validate_csv(
                self.fields, self.csv_dir + '/valid_users.csv', primary_key_field='user_id')
        self.assertEqual(result.valid, True)
        self.assertNotEqual(result.data, None)

    def test_unicode(self):
        result: csv_utils.CsvStatus = csv_utils.validate_csv(
                fields=self.fields,
                file_path=self.csv_dir + '/valid_unicode.csv'
        )

        # If the server does not crash, we assume success
        self.assertEqual(result.valid, True)
        self.assertNotEqual(result.data, None)
        self.assertEqual(result.error_message, None)
        # TODO(egeldenhuys): Test returned data

    # The exception message is only a message, nothing crashed.
    def test_corrupt(self):
        # csv_utils prints when handling corrupt file
        logging.disable(logging.CRITICAL)
        result: csv_utils.CsvStatus = csv_utils.validate_csv(
                fields=self.fields,
                file_path=self.csv_dir + '/invalid_corrupt.csv'
        )
        self.assertEqual(result.valid, False)
        self.assertEqual(result.data, None)
        self.assertNotEqual(result.error_message, None)
        logging.disable(logging.NOTSET)

    def test_corrupt2(self):
        # csv_utils prints when handling corrupt file
        logging.disable(logging.CRITICAL)
        result: csv_utils.CsvStatus = csv_utils.validate_csv(
                fields=self.fields,
                file_path=self.csv_dir + '/invalid_corrupt2.csv'
        )

        self.assertEqual(result.valid, False)
        self.assertEqual(result.data, None)
        self.assertNotEqual(result.error_message, None)
        logging.disable(logging.NOTSET)

    def test_optional_fields(self):
        # Optional fields may be None
        # Non optional cannot be None or empty
        # Only the primary_key_field must be unique and not empty

        # When an optional field is given that is not part of
        # the fields, then an exception is thrown

        self.assertRaises(OptionalKeyNotFoundError,
                          csv_utils.validate_csv,
                          ['pk', 'optional'],
                          'should_not_read_csv.csv',
                          primary_key_field='pk',
                          optional_fields=['should_not_be_found'])

        result: csv_utils.CsvStatus = csv_utils.validate_csv(
                fields=['pk', 'name', 'middle_name', 'last_name'],
                file_path=self.csv_dir + '/valid_optional.csv',
                primary_key_field='pk',
                optional_fields=['middle_name'])

        self.assertEqual(len(result.data), 2)
        self.assertEqual(result.data[0]['pk'], '1')
        self.assertEqual(result.data[0]['name'], 'Fred')
        self.assertEqual(result.data[0]['middle_name'], 'John')
        self.assertEqual(result.data[0]['last_name'], 'Bool')

        self.assertEqual(result.data[1]['pk'], '2')
        self.assertEqual(result.data[1]['name'], 'James')
        self.assertEqual(result.data[1]['middle_name'], '')
        self.assertEqual(result.data[1]['last_name'], 'TheMan')
