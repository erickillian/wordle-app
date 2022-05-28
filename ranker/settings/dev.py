"""
Django settings for ranker project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(SETTINGS_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!os.path.dirname(os.path.realpath(__file__))
SECRET_KEY = 'development_secret_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
# CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'ranker.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSIONS_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication'
    ],
}

ROOT_URLCONF = 'ranker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'dist')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# AUTHENTICATION_BACKENDS = [
#     # Needed to login by username in Django admin, regardless of `allauth`
#     'django.contrib.auth.backends.ModelBackend',

#     # `allauth` specific authentication methods, such as login by e-mail
#     'allauth.account.auth_backends.AuthenticationBackend',
# ]

WSGI_APPLICATION = 'ranker.wsgi.application'

LOGIN_REDIRECT_URL = '/'

ALLOWED_HOSTS = [
    'localhost',
    'localhost:3000',
    # 'localhost:8080',
    # '127.0.0.1',
    # '127.0.0.1:8000',
    # '127.0.0.1:8080',
    # '0.0.0.0'
    # '0.0.0.0:8000',
    # '0.0.0.0:8080',
]

CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://localhost:8080", "http://localhost:3000", "https://converge-general-sports.herokuapp.com"]

SITE_ID = 1

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = (
    'Access-Control-Allow-Origin: *',
)

# CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
# CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = (
#     'http://localhost:8000',  # Django default port = 8000
#     'http://localhost:8080',  # Vue port for frontend dev = 8080
# )

# CSRF_TRUSTED_ORIGINS = [
#     'localhost',
#     'localhost:8000',
#     'localhost:8080',
#     '127.0.0.1',
#     '127.0.0.1:8000',
#     '0.0.0.0'
#     '0.0.0.0:8000',
# ]

# CORS_ALLOWED_ORIGINS = [
#     'localhost',
#     'localhost:8000',
#     'localhost:8080',
#     '127.0.0.1',
#     '127.0.0.1:8000',
#     '0.0.0.0'
#     '0.0.0.0:8000',
# ]




# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ranker',
        'USER': 'ranker',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# LOCALE_PATHS = [
#     os.path.join(BASE_DIR, 'ranker', 'core', 'locale')
# ]

# Extendable user model
AUTH_USER_MODEL = 'core.Player'
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_UNIQUE_EMAIL=True
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED=True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'

ACCOUNT_FORMS = {'signup': 'cire.forms.MyCustomSignupForm'}

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'ranker.core.serializers.RegisterSerializer',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'dist', 'static')]


# Caching stats page
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'default_cache',
    },
    'leaderboard': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'leaderboard_cache',
    }
}
