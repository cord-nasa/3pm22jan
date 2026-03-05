

"""
Django settings for Cord project.
Updated for Render Deployment + Flutter Support + Cloudinary Media Storage
"""
import dj_database_url
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================================
# SECURITY SETTINGS
# =========================================================

# 1. SECRET_KEY: Try to get it from Render. If not found, use the insecure local one.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-g^-g!!08#5_(3agt4+=i=(o@miqp8jhx)4hazka(4c2+%t=z42')

# 2. DEBUG: Disable Debug mode on Render (Production), keep True locally
if 'RENDER' in os.environ:
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ['*'] # Required for Render

# =========================================================
# APPLICATION DEFINITION
# =========================================================

INSTALLED_APPS = [
    # --- CLOUDINARY APPS (Must be before staticfiles if using for static, good practice generally) ---
    'django.contrib.staticfiles',  # Move this to the top of the group
    'cloudinary_storage', 
    'cloudinary',
    'anymail',
    'django.contrib.admin',

    
    
    # --- DEFAULT APPS ---
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    # --- THIRD PARTY APPS ---
    'rest_framework',
    'corsheaders', 
    
    # --- YOUR APPS ---
    'CordApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static file serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',       # CORS headers
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Cord.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Cord.wsgi.application'

# =========================================================
# DATABASE
# =========================================================

DATABASES = {
    'default': dj_database_url.config(
        # Local fallback (SQLite)
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}

# =========================================================
# PASSWORDS & I18N
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =========================================================
# STATIC FILES (CSS, JS)
# =========================================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# This still compresses files but won't crash the entire build if one is missing
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False
# Add these settings to handle missing files gracefully
WHITENOISE_ROOT = os.path.join(BASE_DIR, 'staticfiles')
WHITENOISE_SKIP_MISSING_FILES = True
# =========================================================
# MEDIA FILES (CLOUDINARY CONFIGURATION)
# =========================================================

# This tells Django to use Cloudinary for any ImageField/FileField
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# Standard Media settings (still good to keep for local dev or reference)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================================================
# CORS SETTINGS (For Flutter)
# =========================================================

CORS_ALLOW_ALL_ORIGINS = True 

# =========================================================
# EMAIL SETTINGS
# =========================================================

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_HOST_USER = 'saanandsdb@gmail.com'
# EMAIL_HOST_PASSWORD = os.environ.get('ems_key', 'chhu bboa dizs vfvg') 


# # --- EMAIL SETTINGS (BREVO) ---
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp-relay.brevo.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'a2a616001@smtp-brevo.com'  # From your image
# EMAIL_HOST_PASSWORD = 'gkc0WGsaWpCNKHQ9'  # From your image
# DEFAULT_FROM_EMAIL = 'Your App Name <a2a616001@smtp-brevo.com>'
# # =========================================================
# =========================================================
# EMAIL SETTINGS (ANYMAIL + BREVO API)
# =========================================================

# 1. Set the Anymail Brevo API Backend
EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"

# 2. Configure the Anymail settings
ANYMAIL = {
    # Ensure you have 'BREVO_API_KEY' in your Render Environment Variables
    "BREVO_API_KEY": os.environ.get("BREVO_API_KEY"),
}

# 3. Default sender settings
# IMPORTANT: This email must be verified in your Brevo Dashboard
DEFAULT_FROM_EMAIL = "Enroute App <saanandsdb@gmail.com>"
SERVER_EMAIL = "saanandsdb@gmail.com"


# STRIPE KEYS
# =========================================================
STRIPE_PUBLISHABLE_KEY = "pk_test_your_key_here"
STRIPE_SECRET_KEY = "sk_test_your_secret_key_here"

# settings.py
