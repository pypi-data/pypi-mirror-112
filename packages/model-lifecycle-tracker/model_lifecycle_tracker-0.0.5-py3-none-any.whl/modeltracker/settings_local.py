DATABASE = {
    'engine': 'postgresql+psycopg2://',
    'database': 'modeltracker',
    'username': 'postgres',
    'password': 'docker',
    'host': 'localhost',
    'port': 5432
}

DEBUG = False
LOCAL_DEVEL = False

# If available, import from local settings and override
try:
    from modeltracker.settings_local import *
except Exception:
    pass