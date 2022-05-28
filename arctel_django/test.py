import os
ENV = "dev"
if ENV == "dev":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
if ENV == "prd":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv("DB_USER"),
            'PASSWORD': os.getenv("DB_PASSWORD"),
            'HOST': os.getenv("DB_HOST"),
        }
    }

if ENV == "dev":
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
if ENV == "prd":
    DEFAULT_FILE_STORAGE = 'storages.backends.ftp.FTPStorage'
    FTP_STORAGE_LOCATION = 'ftp://user:password@localhost:21'