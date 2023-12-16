from pathlib import Path

BASE_DIR = Path(__file__).parent

# main
MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'
DOWNLOADS_DIR_NAME = 'downloads'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

# outputs
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
FILE_OUTPUT_DIR_NAME = 'results'

# configs
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
OUTPUT_PRETTY_MODE = 'pretty'
OUTPUT_FILE_MODE = 'file'
LOG_DIR = BASE_DIR / 'logs'
