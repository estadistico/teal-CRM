"""
Django settings for djproj project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g*#m%ohk#f3$5sof44udwbg@me#y$vz&vl^i@kfk44qz@kht&@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'crm',
    'tasks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters'
]

CSRF_TRUSTED_ORIGINS= ['https://teal-crm-production.up.railway.app']
#https://admin.tuprofeestadistica.com
#https://teal-crm-production.up.railway.app/

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djproj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
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

WSGI_APPLICATION = 'djproj.wsgi.application'

# twilio

TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

''' DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', #'ENGINE': 'django.db.backends.mysql', mysql.connector.django
        'HOST': 'containers-us-west-133.railway.app',  # O la dirección IP proporcionada por tu proveedor de hosting 144.126.136.150
        'PORT': 6769,   # Déjalo en blanco para usar el puerto predeterminado de MySQL
        'NAME': 'railway',
        'USER': 'root',
        'PASSWORD':os.environ.get('DBPASSWORD'),
    }
}  
 '''

''' DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', #'ENGINE': 'django.db.backends.mysql', mysql.connector.django
        'HOST': 'tuprofeestadistica.com',  # O la dirección IP proporcionada por tu proveedor de hosting 144.126.136.150
        'PORT': '',           # Déjalo en blanco para usar el puerto predeterminado de MySQL
        'NAME': 'tuprofee_db_admin1',
        'USER': 'tuprofee_cristianc',
        'PASSWORD':os.environ.get('DBPASSWORD'),
    }
}   
'''
## BD de railway

''' DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', #'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD':os.environ.get('DBPASSWORD'),
        'HOST': 'containers-us-west-145.railway.app',  # O la dirección IP proporcionada por tu proveedor de hosting 144.126.136.150
        'PORT': '6304',           # Déjalo en blanco para usar el puerto predeterminado de MySQL
    }
} 
 '''
 
 ## BD de local

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}   



# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT= os.path.join(BASE_DIR,"staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

LOGIN_URL='/signin'
LOGIN_REDIRECT_URL='/signin'