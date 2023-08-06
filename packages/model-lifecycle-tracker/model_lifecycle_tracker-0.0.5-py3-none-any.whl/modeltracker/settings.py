DATABASE = {
    'engine': 'postgresql+psycopg2://',
    'database': 'modeltracker',
    'username': 'username',
    'password': 'password',
    'host': 'localhost',
    'port': 5432
}



DEBUG = False
LOCAL_DEVEL = False

# If available, import from local settings and override
try:
    from settings_local import *
except Exception:
    pass