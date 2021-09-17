THREADS_PER_PAGE = 2
SQLALCHEMY_DATABASE_URI = 'sqlite:///register.db'
MAX_CONTENT_LENGTH = 86 * 1000 * 1000 #Max content size is 86 mb
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOADS_DIR = '' #override this value in the instance config.py with the absolute path the the uploads folder

# Email configuration
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'codingclub@psgtech.ac.in'
MAIL_DEFAULT_SENDER = ('Coding Club PSGCT', MAIL_USERNAME)