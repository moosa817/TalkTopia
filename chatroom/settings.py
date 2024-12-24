"""
Django settings for chatroom project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
from os import getenv
import dj_database_url

GUEST_USER_NAME_GENERATOR = "guest_user.functions.generate_numbered_username"
GUEST_USER_CONVERT_REDIRECT_URL = "home"


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("SECRET_KEY")
SESSION_COOKIE_HTTPONLY = False

# SECURITY WARNING: don't run with debug turned on in production!


DEBUG = True if getenv("DEBUG", None) == "True" else False
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "192.168.18.123",
    "talktopia.vercel.app",
    ".vercel.app",
]


# Application definition

INSTALLED_APPS = [
    "base.apps.BaseConfig",
    "imagekit",
    "storages",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "guest_user",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # it should be the last entry to prevent unauthorized access
    "guest_user.backends.GuestBackend",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "chatroom.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

ASGI_APPLICATION = "chatroom.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# this gets overwritten
DATABASES = {"default": {}}

# requires a env for db str (using postgressql)

DATABASES["default"] = dj_database_url.config(conn_max_age=600, ssl_require=False)


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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# aws s3bucket config

AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = getenv("AWS_STORAGE_BUCKET_NAME")
CLOUDFRONT_DOMAIN = getenv("CLOUDFRONT_DOMAIN")

AWS_QUERYSTRING_EXPIRE = 604800

AWS_S3_SIGNATURE_NAME = ("s3v4",)
AWS_S3_REGION_NAME = "us-east-1"
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_CUSTOM_DOMAIN = CLOUDFRONT_DOMAIN


if DEBUG == False:
    STATIC_LOCATION = "static"
    STATIC_URL = f"{CLOUDFRONT_DOMAIN}/static/"
    # Add your path in the STATICFILES_STORAGE
    STATICFILES_STORAGE = "chatroom.storage_backends.StaticStorage"
else:
    STATIC_URL = "static/"


# CUSTOM SECRETS

EMAIL_SENDER = getenv("EMAIL_SENDER")
MAIL_PWD = getenv("SMTP_PWD")
MAIL_EMAIL_RECIVER = getenv("EMAIL_RECIEVER")
MAIL_SERVER = getenv("MAIL_SERVER")
MAIL_PORT = 587
MAIL_USER = getenv("MAIL_USER")


# other settings
WS_URL = getenv("WS_URL")
ROOM_PAGE = int(getenv("ROOM_PAGE"))  # rooms to show per page
MESSAGE_ROOM = int(getenv("MESSAGE_ROOM"))  # messages to show per room
