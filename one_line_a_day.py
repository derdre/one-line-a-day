import argparse
import os
from datetime import date, datetime, timedelta
from shutil import rmtree

# argument parser
parser = argparse.ArgumentParser(
    description='Python script to generate a folder structure for one line a day.'
)
parser.add_argument(
    '--path',
    help='Define path where folder structure is generated',
    type=str,
    default='one_line_a_day',
)
parser.add_argument(
    '--years',
    help='For how many years would you like to generate file entries?',
    type=int,
    default=5,
)
args = parser.parse_args()

PATH = args.path
YEARS = args.years

# folder string definitions
month_strings = [
    '01-January',
    '02-February',
    '03-March',
    '04-April',
    '05-May',
    '06-June',
    '07-July',
    '08-August',
    '09-September',
    '10-October',
    '11-November',
    '12-December',
]


def create_tree(path, years, current_date, month_strings):
    """
    Create the file tree according to present date
    - one_line_a_day
        - 01-January
            - 01-jan.md
            - 02-jan.md
            - ...
        - 02-February
        - ...
    """

    # present year
    year = current_date.year
    start_date = date(year, 1, 1)
    end_date = date(year + years - 1, 12, 31)

    # check for existing path
    if os.path.exists(path):
        rmtree(path)

    # generate the path PATH and subfolders
    os.mkdir(path)
    os.chdir(path)
    for folder in month_strings:
        os.mkdir(folder)

    delta = timedelta(days=1)
    while start_date <= end_date:
        m = start_date.month - 1  # counting from 0 (zero)
        d = start_date.strftime('%d')
        m_str = start_date.strftime('%b').lower()
        y = start_date.strftime('%Y')

        # define formated strings
        file_path = month_strings[m] + '/' + d + '-' + m_str + '.md'
        header = '### ' + d + '-' + m_str + '-' + y + ': *loc*\n'
        placeholder = '<line>\n'

        # write to file
        file = open(file_path, 'a')  # append to file
        file.write(header)
        file.write(placeholder)
        file.write('\n')
        file.close()

        # increment variable
        start_date += delta

    return 'done'


if __name__ == '__main__':
    current_date = datetime.now()
    create_tree(PATH, YEARS, current_date, month_strings)
