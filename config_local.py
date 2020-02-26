from dateutil.relativedelta import relativedelta

MYSQL_USER = 'root'
MYSQL_PASSWORD = '123'
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_DB = 'newsapi'
DB_NAME = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

SQLALCHEMY_DATABASE_URI = DB_NAME
SQLALCHEMY_TRACK_MODIFICATIONS = False,
PROPAGATE_EXCEPTIONS = True,
JSONIFY_PRETTYPRINT_REGULAR = True,
JSON_SORT_KEYS = False
JWT_BALCKLIST_ENABLED = True  # Enable JWT  Blacklist
JWT_BLACKLIST_CHECKS = ['access', 'refresh']
JWT_SECRET_KEY = 'test'
JWT_ACCESS_TOKEN_EXPIRES = relativedelta(days=1)
REDIS_URL = 'redis://host:6379/0'


