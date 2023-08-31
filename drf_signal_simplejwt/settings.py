"""
Django settings for drf_signal_simplejwt project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta

from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DJANGO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY', 'django-insecure-wc&2fs)##e8o5d1=!#4$z_jv_*^$5t*_x=!jm3v!x1r(1ss&ee'))
# SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-wc&2fs)##e8o5d1=!#4$z_jv_*^$5t*_x=!jm3v!x1r(1ss&ee')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.getenv('DEBUG', 'True') == "True"
# DEBUG = bool(int(os.getenv('DEBUG')))

ALLOWED_HOSTS = ['*']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

API_KEY = str(os.getenv('API_KEY', '123456'))

AUTH_USER_MODEL = 'users.UserDetail'

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'background_task',    # `migrate` needed.
    'dj_scheduler',
    'auditlog',    # `migrate` needed.
    # 'rest_framework.authtoken',
    # 'knox',
    "master",
    "users",
    # "users.apps.AppConfig",    # ! Signal (1/3) (Optional) - Just add the app name where the signal is registered. In this case its `users`.
]

CORS_ORIGIN_ALLOW_ALL = True

# CSRF_TRUSTED_ORIGINS = ['*']

X_FRAME_OPTIONS = 'SAMEORIGIN'     # Only if django version >= 3.0

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "drf_signal_simplejwt.middleware.SubscriptionMiddleware",
]

ROOT_URLCONF = "drf_signal_simplejwt.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "drf_signal_simplejwt.wsgi.application"

# ASGI_APPLICATION = "drf_signal_simplejwt.routing.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.environ.get('DB_NAME', 'dj_signal'),
        'USER': os.environ.get('DB_USER', 'root'),
        # 'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '123456'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        # 'PORT': os.environ.get('DB_PORT', '5432')
        'OPTIONS' if not os.path.exists(os.path.join(DJANGO_ROOT, '.env')) else '' : {
            'sql_mode': 'traditional',
        } if not os.path.exists(os.path.join(DJANGO_ROOT, '.env')) else '',
    }
}

print("### CONNECTED DATABASE AT SERVER '{}' HAVING PORT '{}' WITH USER '{}' ON DATABASE '{}' ###".format(
                                                                                            DATABASES['default']['HOST'],
                                                                                            DATABASES['default']['PORT'],
                                                                                            DATABASES['default']['USER'],
                                                                                            DATABASES['default']['NAME']))


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        # 'knox.auth.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
    # 'EXCEPTION_HANDLER':'exceptions.root_simple_error_handler'
}


STATIC_ROOT_PATH = str(os.getenv('STATIC_ROOT_PATH'))
STATIC_ROOT = os.path.join(STATIC_ROOT_PATH, 'static')
STATIC_URL = os.path.join(str(os.getenv('STATIC_MEDIA_SERVER_HOST')), 'static/')

MEDIA_ROOT_PATH = str(os.getenv('MEDIA_ROOT_PATH'))
MEDIA_ROOT = os.path.join(MEDIA_ROOT_PATH, "media")
MEDIA_URL = os.path.join(str(os.getenv('STATIC_MEDIA_SERVER_HOST')), 'media/')
MEDIA_ROOT_EXPORT = os.path.join(MEDIA_ROOT_PATH, "")

SERVER_HOST = str(os.getenv('SERVER_HOST'))
SERVER_URL = str(os.getenv('SERVER_URL'))
SERVER_API_URL = str(os.getenv('SERVER_API_URL'))


# Default Messages
MSG_SUCCESS="Success"
MSG_NO_DATA="No Data Found"
MSG_ERROR="Failure"


from os.path import abspath, basename, dirname, join, normpath

LOG_ROOT = os.path.join(DJANGO_ROOT, "logs")
if not os.path.exists(LOG_ROOT):
    os.makedirs(LOG_ROOT)

if not os.path.exists(LOG_ROOT + "/django"):
    os.makedirs(LOG_ROOT + "/django")
if not os.path.exists(LOG_ROOT + "/django/debug"):
    os.makedirs(LOG_ROOT + "/django/debug")
if not os.path.exists(LOG_ROOT + "/django/critical"):
    os.makedirs(LOG_ROOT + "/django/critical")
if not os.path.exists(LOG_ROOT + "/django/error"):
    os.makedirs(LOG_ROOT + "/django/error")
if not os.path.exists(LOG_ROOT + "/django/info"):
    os.makedirs(LOG_ROOT + "/django/info")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] [%(module)s.%(funcName)s] [%(process)d.%(thread)d] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(DJANGO_ROOT, 'logs/django/debug/django_debug.log'),
            'maxBytes': 1024 * 1024 * 2, # Max 2 MB
            #'when': 'D', # this specifies the interval
            #'interval': 1, # defaults to 1, only necessary for other values 
            'backupCount': 1, # how many backup file to keep, 9 hrs
            'formatter': 'verbose',
        },
        # 'filecritical': {
        #     'level': 'CRITICAL',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': os.path.join(self.DJANGO_ROOT, 'logs/django/critical/django_critical.log'),
        #     'maxBytes': 1024 * 1024 * 2, # Max 2 MB
        #     #'when': 'D', # this specifies the interval
        #     #'interval': 1, # defaults to 1, only necessary for other values 
        #     'backupCount': 1, # how many backup file to keep, 9 hrs
        #     'formatter': 'verbose',
        # },
        'fileerror': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(DJANGO_ROOT, 'logs/django/error/django_error.log'),
            'maxBytes': 1024 * 1024 * 2, # Max 2 MB
            #'when': 'D', # this specifies the interval
            #'interval': 1, # defaults to 1, only necessary for other values 
            'backupCount': 1, # how many backup file to keep, 9 hrs
            'formatter': 'verbose',
        },
        'fileinfo': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(DJANGO_ROOT, 'logs/django/info/django_info.log'),
            'maxBytes': 1024 * 1024 * 2, # Max 2 MB
            #'when': 'D', # this specifies the interval
            #'interval': 1, # defaults to 1, only necessary for other values 
            'backupCount': 1, # how many backup file to keep, 9 hrs
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
        # 'myproject.custom':{
        #     'handlers': ['filecritical'],
        #     'level': os.getenv('DJANGO_LOG_LEVEL', 'CRITICAL'),
        # },
        'django.request':{
            'handlers': ['fileerror'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
        '': {
            'handlers': ['fileinfo'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        }
    },
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


NEW_USER_DEFAULT_PASSWORD = str(os.getenv('NEW_USER_DEFAULT_PASSWORD', '123456'))

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME' : timedelta(minutes=120),       # ? Access Token life time, Default: 5 mins. [KEEP THIS VALUE LOW FOR SECURITY REASONS].
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=60),        # ? Allows the access token's expiration to be extended each time it is used to hit an API before the access token expires. This feature is useful to keep the user session active as long as they are actively using the application, as long as the refresh token is valid.
    'REFRESH_TOKEN_LIFETIME' : timedelta(days=7),           # ? Refresh Token life time, Default: 1 day.
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),    # ? When a new access token is generated using a refresh token, the expiration time of the refresh token is extended by this value. If the refresh token is not used to obtain a new access token within this period, it becomes inactive. This mechanism allows for sliding token expiration, meaning that as long as the user keeps using the application, their token remains valid. Default: 1 day.
    'AUTH_HEADER_TYPES': ('JWT',),                          # ? Used to specify the authentication type that should be used for JWT (JSON Web Token) authentication. By default, the Django REST framework expects the JWT token to be sent in the request header with the type 'Bearer'. However, if you set 'JWT' in AUTH_HEADER_TYPES, it will expect the token to be sent with the type 'JWT'. Use in Headers, `Authorization : JWT <token here>`, by default its, `Authorization : Bearer <token here>`.
    'ROTATE_REFRESH_TOKENS' : False,                        # ? When set to `True`, each time a refresh token is used, a new one is returned. The old refresh token will continue to work until it expires. Default is `False`. If you want to use this feature, you will also need to set `BLACKLIST_AFTER_ROTATION` to `True`. Otherwise, there will be a lot of refresh tokens.
    'BLACKLIST_AFTER_ROTATION' : True,                      # If set to `True`, refresh tokens will be blacklisted if new access token is generated from it. Defaults to `False`.
    'ALGORITHM': 'HS256',                                   # HMAC-SHA256. This is the default value.
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',       # Default: 'refresh_exp', The claim name to use for the token expiration time when using sliding token expiration.  This setting allows you to customize the name of the claim in the refresh token that holds the token's expiration time.  If you want to change the claim name to something other than the default, you can set this value to your preferred claim name.
}

'''
from datetime import timedelta
# from rest_framework.settings import api_settings
REST_KNOX = {
	'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
	'AUTH_TOKEN_CHARACTER_LENGTH': 64,
	'TOKEN_TTL': timedelta(hours=12),    # Token never expire if set to `None`.
	'USER_SERIALIZER': 'knox.serializers.UserSerializer',
	'TOKEN_LIMIT_PER_USER': None,
	'AUTO_REFRESH': False,
	#'EXPIRY_DATETIME_FORMAT': api_settings.DATETME_FORMAT,
}
'''

