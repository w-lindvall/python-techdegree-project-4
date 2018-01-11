import unittest

from peewee import *


class TestWorklog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from work_log import Entry
        WL_DATABASE = SqliteDatabase('work_log.db')
        WL_DATABASE.connect()
        WL_DATABASE.create_tables([Entry], safe=True)

    def test_add_entry(self):
        from work_log import add_entry
        test_entry = add_entry('Test Name', 'Test Title', '2', 'Test Notes')
        self.assertEqual(test_entry.employee_name, 'Test Name')
        test_entry.delete_instance()

    def test_get_unique_employees(self):
        from work_log import get_unique_employees, add_entry
        test_entry = add_entry('Test Name', 'Test Title', '2', 'Test Notes')
        unique_names = get_unique_employees()
        self.assertTrue(unique_names)
        test_entry.delete_instance()

    def test_get_unique_dates(self):
        from work_log import get_unique_dates, add_entry
        test_entry = add_entry('Test Name', 'Test Title', '2', 'Test Notes')
        unique_dates = get_unique_dates()
        self.assertTrue(unique_dates)
        test_entry.delete_instance()

    def test_check_for_entries(self):
        from work_log import check_for_entries, add_entry
        test_entry = add_entry('Test Name', 'Test Title', '2', 'Test Notes')
        self.assertTrue(check_for_entries)
        test_entry.delete_instance()

    def test_check_for_filtered_entries(self):
        from work_log import check_for_filtered_entries
        found_filtered_entries = ['Entry1', 'Entry2', 'Entry3']
        no_filtered_entries = []
        self.assertTrue(check_for_filtered_entries(found_filtered_entries))
        self.assertFalse(check_for_filtered_entries(no_filtered_entries))

    def test_validate_menu_input(self):
        from work_log import validate_menu_input
        self.assertTrue(validate_menu_input('a'))
        self.assertTrue(validate_menu_input('b'))
        self.assertFalse(validate_menu_input('e'))
        self.assertFalse(validate_menu_input(''))

    def test_validate_name_input(self):
        from work_log import validate_name_input
        self.assertTrue(validate_name_input('Bob'))
        self.assertFalse(validate_name_input(''))
        self.assertFalse(validate_name_input('Bob_Anderson'))
        self.assertFalse(validate_name_input('12'))

    def test_validate_title_input(self):
        from work_log import validate_title_input
        self.assertTrue(validate_title_input('Swim'))
        self.assertFalse(validate_title_input(''))

    def test_validate_duration_input(self):
        from work_log import validate_duration_input
        self.assertTrue(validate_duration_input('90'))
        self.assertFalse(validate_duration_input('90 minutes'))
        self.assertFalse(validate_duration_input('Two'))

    def test_validate_notes_input(self):
        from work_log import validate_notes_input
        self.assertEqual(validate_notes_input('Good times'), 'Good times')
        self.assertEqual(validate_notes_input(''), 'None')

    def test_validate_lookup_menu_input(self):
        from work_log import validate_lookup_menu_input
        self.assertTrue(validate_lookup_menu_input('a'))
        self.assertFalse(validate_lookup_menu_input('e'))

    def test_validate_lookup_employee_format(self):
        from work_log import validate_lookup_employee_format
        self.assertTrue(validate_lookup_employee_format('Bob'))
        self.assertFalse(validate_lookup_employee_format(''))

    def test_validate_lookup_date_format(self):
        from work_log import validate_lookup_date_format
        self.assertTrue(validate_lookup_date_format('24/12/2014'))
        self.assertFalse(validate_lookup_date_format('24/15/2014'))

    def test_validate_lookup_time_spent_format(self):
        from work_log import validate_lookup_time_spent_format
        self.assertTrue(validate_lookup_time_spent_format('90'))
        self.assertFalse(validate_lookup_time_spent_format('Two'))

    def test_validate_lookup_search_term_format(self):
        from work_log import validate_lookup_search_term_format
        self.assertTrue(validate_lookup_search_term_format('Stuff'))
        self.assertFalse(validate_lookup_search_term_format(''))


if __name__ == '__main__':
    unittest.main()
