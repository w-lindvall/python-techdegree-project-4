"""Work Log with Database
Add and search employee work tasks using a database.

Created: 20 November, 2017
Last updated: 26 November, 2017
Author: William Lindvall
"""

from collections import OrderedDict
import datetime
import os

from peewee import *


WL_DATABASE = SqliteDatabase('work_log.db')


class Entry(Model):
    """Model describing work_log.db entry information"""
    timestamp = DateTimeField(default=datetime.datetime.today()
                              .strftime('%d/%m/%Y'))
    employee_name = TextField()
    task_title = TextField()
    time_spent = IntegerField()
    task_notes = TextField()

    class Meta:
        database = WL_DATABASE


def clear():
    """Clear screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """Main menu loop"""
    clear()
    choice = None
    while choice != 'q':
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('> ').lower().strip()
        if choice == 'q':
            break
        if validate_menu_input(choice):
            menu[choice]()


def validate_menu_input(choice):
    """Ensures main menu input is valid"""
    if choice in menu.keys():
        clear()
        return True

    else:
        clear()
        print('** Please enter \'a\', \'b\', or \'q\' to quit **')
        return False


def new_entry():
    """Create new entry"""
    while True:
        name = input('Employee name: ').strip()
        if validate_name_input(name):
            break
    while True:
        title = input('Task title: ').strip()
        if validate_title_input(title):
            break
    while True:
        duration = input('Time spent (in minutes): ').strip()
        if validate_duration_input(duration):
            break
    notes = input('Notes (optional): ').strip()
    validate_notes_input(notes)
    add_entry(name, title, duration, notes)


def validate_name_input(name):
    """Ensures employee name input is valid"""
    if all(letter.isalpha() or letter.isspace()
           for letter in name) and len(name) != 0:
        clear()
        return True

    else:
        clear()
        print('** Please enter a name of alphabetic characters and spaces **')
        return False


def validate_title_input(title):
    """Ensures task title input is valid"""
    if len(title) != 0:
        clear()
        return True

    else:
        clear()
        print('** Please enter a task title **')
        return False


def validate_duration_input(duration):
    """Ensures task duration input is valid"""
    if duration.isdigit():
        duration = int(duration)
        clear()
        return duration

    else:
        clear()
        print('** Please enter time spent on task '
              'rounded to nearest whole minute **')
        return False


def validate_notes_input(notes):
    """Checks task note input"""
    if len(notes) == 0:
        notes = 'None'
    clear()
    return notes


def add_entry(name, title, duration, notes):
    """Adds entry to work log database"""
    clear()
    print('Entry added to work log!')
    return Entry.create(
        employee_name=name,
        task_title=title,
        time_spent=duration,
        task_notes=notes
    )


def lookup_entries():
    """Lookup existing entries"""
    if check_for_entries():
        choice = None
        while choice != 'q':
            for key, value in lookup_menu.items():
                print('{}) {}'.format(key, value.__doc__))
            choice = input('> ').lower().strip()
            if choice == 'q':
                clear()
                break
            elif validate_lookup_menu_input(choice):
                filtered_entries = lookup_menu[choice]()
                if not check_for_filtered_entries(filtered_entries):
                    input('Press enter to return to main menu.')
                for entry in filtered_entries:
                    timestamp = entry.timestamp
                    print('=' * 25 + '\n'
                                     'Date: ' + timestamp +
                          '\nEmployee name: ' + entry.employee_name +
                          '\nTask: ' + entry.task_title +
                          '\nDuration: ' + str(entry.time_spent) + ' minutes' +
                          '\nNotes: ' + entry.task_notes + '\n' + '=' * 25
                          )
                    print('N) next entry\nq) quit to main menu')
                    choice = input('> ').lower().strip()
                    if choice == 'q':
                        clear()
                        break
                    clear()


def check_for_entries():
    """Returns True if entries exist. If none, returns False."""
    if Entry.select():
        return True

    else:
        clear()
        input('** Woops! Looks like there are no entries to lookup **\n'
              'Press enter to return to main menu.')


def check_for_filtered_entries(filtered_entries):
    """Returns False if lookup returns no entries. Else, returns True"""
    if len(filtered_entries) == 0:
        clear()
        print('Woops! Your search didn\'t return any entries.')
        return False

    else:
        clear()
        return True


def validate_lookup_menu_input(choice):
    """Ensures choice from lookup menu is valid"""
    if choice in lookup_menu.keys():
        clear()
        return True

    else:
        clear()
        print('** Please enter \'a\', \'b\', \'c\', '
              '\'d\' or \'q\' to return to main menu **')
        return False


def lookup_employee():
    """Lookup by employee name"""
    unique_names = get_unique_employees()
    while True:
        if len(unique_names) > 1:
            print('Entries found by {} and {}.'.format(
                ', '.join(unique_names[:-1]),
                unique_names[-1]))
        elif len(unique_names) == 1:
            print('Entries found by {}.'.format(unique_names[0]))

        search_query = input('Show entries by: ')
        if validate_lookup_employee_format(search_query):
            break
        print('** Please enter a name of alphabetic characters and spaces **')
    return Entry.select().where(Entry.employee_name == search_query)


def get_unique_employees():
    """Finds list of unique employee names with entries"""
    unique_names = []

    for entry in Entry.select():
        if entry.employee_name not in unique_names:
            unique_names.append(entry.employee_name)

    clear()
    return unique_names


def validate_lookup_employee_format(search_query):
    """Ensures employee name input is valid"""
    if (all(letter.isalpha() or letter.isspace() for letter in
            search_query) and len(search_query) != 0):
        clear()
        return True

    else:
        clear()
        return False


def lookup_date():
    """Lookup by date"""
    unique_dates = get_unique_dates()
    while True:
        if len(unique_dates) > 1:
            print('Entries found for {} and {}.'.format(
                ', '.join(unique_dates[:-1]),
                unique_dates[-1]))
        elif len(unique_dates) == 1:
            print('Entries found for {}.'.format(unique_dates[0]))

        search_query = input('Show entries for (DD/MM/YYYY): ')
        if validate_lookup_date_format(search_query):
            break
        print('** Please enter date in format DD/MM/YYYY **')
    return Entry.select().where(Entry.timestamp == search_query)


def get_unique_dates():
    """Finds list of unique dates of entries"""
    unique_dates = []

    for entry in Entry.select():
        if entry.timestamp not in unique_dates:
            unique_dates.append(entry.timestamp)

    clear()
    return unique_dates


def validate_lookup_date_format(search_query):
    """Ensures task date input is valid"""
    try:
        datetime.datetime.strptime(search_query, '%d/%m/%Y')
        clear()
        return search_query

    except ValueError:
        clear()
        return False


def lookup_time_spent():
    """Lookup by time spent"""
    while True:
        search_query = input('Show entries in which time spent '
                             '(in minutes) is: ')
        if validate_lookup_time_spent_format(search_query):
            break
        print('** Please enter positive integer **')
    return Entry.select().where(Entry.time_spent == search_query)


def validate_lookup_time_spent_format(search_query):
    """Ensures task duration input is valid"""
    if search_query.isdigit():
        clear()
        return int(search_query)

    else:
        clear()
        return False


def lookup_search_term():
    """Lookup by search term"""
    while True:
        search_query = input('Show entries containing (in name or notes): ')
        if validate_lookup_search_term_format(search_query):
            break
        print('** Please enter search term **')
    return (Entry.select().where(Entry.employee_name.contains(search_query)) |
            Entry.select().where(Entry.task_notes.contains(search_query)))


def validate_lookup_search_term_format(search_query):
    """Ensures search term input is valid"""
    if len(search_query) != 0:
        clear()
        return True

    else:
        clear()
        return False


menu = OrderedDict([
    ('a', new_entry),
    ('b', lookup_entries)
])

lookup_menu = OrderedDict([
    ('a', lookup_employee),
    ('b', lookup_date),
    ('c', lookup_time_spent),
    ('d', lookup_search_term)
])


if __name__ == '__main__':
    WL_DATABASE.connect()
    WL_DATABASE.create_tables([Entry], safe=True)

    menu_loop()
