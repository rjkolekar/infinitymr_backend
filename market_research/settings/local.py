from ..base import *
from pathlib import Path

SECRET_KEY = "f#^st#9-kvv&c3pilne=tjv1$-vauyl@q3$$-yzkn6y0x3jdg#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database settings for app
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "infinity_db",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "USER": "root",
        "PASSWORD": "reset@123",
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'market_research',
#         'USER': 'root',
#         'PASSWORD': 'reset123',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

BASE_DIR = Path(__file__).resolve().parent.parent
# # 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

CLIENT_ID = "P4Q4ZFCTLn6tBgC0byExMuiETHce5PIKkZEGjGxD"
CLIENT_SECRET = "5RjNUpkuFeo5QKKdBu6YcahgiRhTPNu3vOAUI693aoILX7tvZXEDLPd9DkaKIjPuKFE3gyQsPAXsd8Tfqkrjbdp9Phi0QMkYPpgzercJYQsXx1nnBJZpWvyjhjyzIHUy"

SERVER_PROTOCOLS = "http://"

# ADMIN_EMAIL = "stark.official123@gmail.com"
# FROM_EMAIL = "joetac4@gmail.com"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "joetac4@gmail.com"
EMAIL_HOST_PASSWORD = "fbfwoyetydrkadqp"
EMAIL_PORT = 587
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True

CC = []
S_KEY = b"ImmOpwdpqo5ALKyjzTOKkJeHihu0i9U4qN3XP2yx_jg="

FRONT_END_URL = "http://127.0.0.1:8000/"
BASE_URL = "http://127.0.0.1:8000/api/v1/"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath("media")

# MEDIA_ROOT = BASE_DIR + "/media/"
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")