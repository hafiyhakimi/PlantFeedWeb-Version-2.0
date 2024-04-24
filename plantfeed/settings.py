"""
Django settings for plantfeed project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p0%y%2(0)#++cz1_tjtn)4j8m#r6)r&%*1$w0*nuqmnx9xsly_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '10.206.96.95', '127.0.0.1', '172.20.10.2']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'member.apps.MemberConfig',
    'sharing.apps.SharingConfig',
    'group.apps.GroupConfig',
    'marketplace.apps.MarketplaceConfig',
    'basket.apps.BasketConfig',
    'payment.apps.PaymentConfig',
    'orders.apps.OrdersConfig',
    'topic.apps.TopicConfig',
    'django.contrib.sites',
    'mathfilters',
    'oauth2_provider',
    'plantfeed',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'plantfeed.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'plantfeed.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oauthfarming',
        'USER':'root',
        'PASSWORD':'',
        'HOST':'localhost',
        'PORT':'3306',
        'OPTIONS':{
            'init_command':"SET sql_mode='STRICT_TRANS_TABLES'",
        }
    },
    # 'farming': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'farming',
    #     'USER':'root',
    #     'PASSWORD':'',
    #     'HOST':'localhost',
    #     'PORT':'3306',
    #     'OPTIONS':{
    #         'init_command':"SET sql_mode='STRICT_TRANS_TABLES'",
    #     }
    # }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

#Encryption
ENCRYPT_KEY = b'tes4-Vdc4kwat6Uz_x0cNSAQ78EXUm3jt3gS1RWMYd4='

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'media'),
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'Home', 'HomeAdmin', 'custom_oauth_authorization'
LOGIN_URL = 'Loginpage', 'plantlinklogin'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ]
}

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        # Add more scopes as needed
    },
    'CLIENT_ID': 'TeoEbwMZQWGf4TGlCbpFmtKxfRyOxS1RCSwV19bH',  # Replace with your client ID
    'CLIENT_SECRET': 'pbkdf2_sha256$600000$sni5XkXIL5Vs7MMF0LJthO$0d78eulHxxit4wabYdGQ++QjwSjxvRHlac5rbA635Uw=',  # Replace with your client secret
}

AUTHENTICATION_CLASSES = (
    # ...
    'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    # ...
)

AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
    # ...
)

# Define your OAuth2 scopes (if needed)
OAUTH2_PROVIDER_SCOPES = {
    'read': 'Read access',
    'write': 'Write access',
    # Add more scopes as needed
}

AUTH_USER_MODEL = 'member.Person'

OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'

OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = 'oauth2_provider.AccessToken'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Default.primary.key.field.type
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

os.environ.setdefault('STRIPE_PUBLISHABLE_KEY', 'pk_test_51M4MnSIMiEP0GJmrTjOFwVfxpZ5KRfUJfHYNTfiEHQ1TlwaQBJxclgibBE0VBYeRRJs85bnPAH0bAzytGUdeqB6i00TbB5FJ8Y')
STRIPE_SECRET_KEY = 'sk_test_51M4MnSIMiEP0GJmrJOwq2TQrafZ2oqouLNRedS8aU0uIqv47JtlR2Hf9lktkAjMbNcvuKbHkcFX6s5DBERkjJ83E00Tr4qRj14'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field


