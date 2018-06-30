import os

app_name = 'django_tagify'

SECRET_KEY = '3902krk23r0k-dfkoa023-r30l0rks'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Installed apps
INSTALLED_APPS = [
    'django_tagify'
]

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'django_tagify/static')

