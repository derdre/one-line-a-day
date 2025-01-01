import argparse
import logging
import shutil
from datetime import date, datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(
    description=(
        'Generate one file for each day of the year. '
        'With a placeholder for daily journaling.'
    )
)
parser.add_argument(
    '--path',
    help='Path where files are created or modified',
    type=Path,
    default='one_line_a_day',
)
parser.add_argument(
    '--years',
    help='Amount of years added to the files',
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


def work_tree(
    path: Path, num_years: int, current_date: datetime, month_strings: list[str]
) -> None:
    """
    Either create or append to file tree according to present date
    - one_line_a_day
        - 01-January
            - 01-jan.md
            - 02-jan.md
            - ...
        - 02-February
        - ...
    """
    year = current_date.year
    start_date = date(year, 1, 1)
    end_date = date(year + num_years - 1, 12, 31)
    delta = timedelta(days=1)

    if path.exists():
        logger.info(f'{path} already exists. Create a backup.')
        backup_path = path.parent / f'{path.parts[-1]}_backup'
        shutil.copytree(path, backup_path, dirs_exist_ok=True)
    else:
        logger.info(f'Create tree at {path}.')
        path.mkdir()
        for folder in month_strings:
            (path / folder).mkdir()

    while start_date <= end_date:
        m = start_date.month - 1  # counting from 0 (zero)
        d = start_date.strftime('%d')
        m_str = start_date.strftime('%b').lower()
        y = start_date.strftime('%Y')

        file_name = d + '-' + m_str + '.md'
        file_path = path / month_strings[m] / file_name
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


if __name__ == '__main__':
    current_date = datetime.now()
    work_tree(PATH, YEARS, current_date, month_strings)
