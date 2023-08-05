# django-project-backup

Django project backup application.

(This is alpha software and is under heavy development)


## Setup

Add the following lines to *settings.py*

```python
# django
INSTALLED_APPS += [
    'django_project_backup'
]

# django-project-backup
SERIALIZATION_MODULES = {
    'dpb_couchdb_datastore': 'django_project_backup.utils.couchdb.serializers'
}

DJANGO_PROJECT_BACKUP_MODE = env('DJANGO_PROJECT_BACKUP_MODE', default='incremental')

DJANGO_PROJECT_BACKUP_PROJECT_NAME = env('DJANGO_PROJECT_BACKUP_PROJECT_NAME', default='django_project_backup')
DJANGO_PROJECT_BACKUP_SHARD_NAME = env('DJANGO_PROJECT_BACKUP_SHARD_NAME', default='1')

# realtime
DJANGO_PROJECT_BACKUP_REALTIME = env.bool('DJANGO_PROJECT_BACKUP_REALTIME', default=True)
DJANGO_PROJECT_BACKUP_DO_REALTIME_COUCHDB_BACKUP = env.bool('DJANGO_PROJECT_BACKUP_DO_REALTIME_COUCHDB_BACKUP',
                                                            default=True)
DJANGO_PROJECT_BACKUP_DO_REALTIME_LOG_BACKUP = env.bool('DJANGO_PROJECT_BACKUP_DO_REALTIME_LOG_BACKUP',
                                                        default=True)

DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS = env.list('DJANGO_PROJECT_BACKUP_EXCLUDED_MODELS', default=[
    'sessions.session',
    'admin.logentry',
    'django_sso_app.passepartout',
    'django_sso_app.device',
    'easy_thumbnails.thumbnail'
])

DJANGO_PROJECT_BACKUP_PUBLIC_ASSETS_FOLDERS = env.list('DJANGO_PROJECT_BACKUP_PUBLIC_ASSETS_FOLDERS',
                                                        default=[str(PUBLIC_ROOT)])

DJANGO_PROJECT_BACKUP_PRIVATE_ASSETS_FOLDERS = env.list('DJANGO_PROJECT_BACKUP_PRIVATE_ASSETS_FOLDERS',
                                                        default=[str(PRIVATE_ROOT)])

DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER = env('DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER',
                                               default=os.path.join(ROOT_DIR, 'backups'))

DJANGO_PROJECT_BACKUP_COUCHDB_DATASTORE_URL = env('DJANGO_PROJECT_BACKUP_COUCHDB_DATASTORE_URL', default='http://127.0.0.1:5984')
DJANGO_PROJECT_BACKUP_COUCHDB_DATASTORE_USER = env('DJANGO_PROJECT_BACKUP_COUCHDB_DATASTORE_USER', default='admin')
DJANGO_PROJECT_BACKUP_COUCHDB_DATASTORE_PASSWORD = env('DJANGO_PROJECT_BACKUP_COUCHDB_DATASTORE_PASSWORD', default='couchdb')
# couchdb db index
DJANGO_PROJECT_BACKUP_COUCHDB_DATASTORE_DATABASE_NAME = env('DJANGO_PROJECT_BACKUP_COUCHDB_DATASTORE_DATABASE_NAME',
                                                            default='django_project_backup')

DJANGO_PROJECT_BACKUP_DO_FAILSAFE_BACKUP = env.bool('DJANGO_PROJECT_BACKUP_DO_FAILSAFE_BACKUP',
                                                    default=True)
DJANGO_PROJECT_BACKUP_FAILSAFE_BACKUP_PATH = env('DJANGO_PROJECT_BACKUP_FAILSAFE_BACKUP_PATH',
                                                 default=os.path.join(DJANGO_PROJECT_BACKUP_DESTINATION_FOLDER, 'failed'))

# log realtime
LOGGING = {
    ...

    "formatters": {
        "dpb_serialized_model": {
            "format": "%(message)s"
        }
    },
    'handlers': {
        "dpb_realtime_log_backup_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(ROOT_DIR, "logs", "django_project_backup.realtime.log"),
            "maxBytes": 1024 * 1024 * 4000,  # 4GB
            "backupCount": 10,
            "formatter": "dpb_serialized_model",
        },
    },
    'loggers': {
        ...

        'django_project_backup.backup_logger': {
            'handlers': ['dpb_realtime_log_backup_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# django-filer
# store files as payload
FILER_DUMP_PAYLOAD = True
```


## Usage

### Filesystem

- Backup DB

    ```
    $ python manage.py dpb_filesystem_dumpdata
    ```

- Backup assets

    ```
    $ python manage.py dpb_filesystem_assets_backup
    ```

### Couchdb

- Backup all

    ```
    $ python manage.py dpb_couchdb_dumpdata
    ```

- Restore all

    ```
    $ python manage.py dpb_couchdb_loaddata
    ```

## Sandbox

### Docker

#### Dependencies
* [Docker](https://docs.docker.com/engine/installation/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Installation
Run the following commands:

```bash
git clone https://bitbucket.org/pai/django-project-backup.git
cd django-project-backup
# build containers
docker-compose up --build -d
# start containers
docker-compose up
# load initial data
docker-compose run app /venv/bin/python manage.py load_initial_data
# perform first backup
docker-compose run app /venv/bin/python manage.py dbp_couchdb_dumpdata
```

The demo site will now be accessible at [http://localhost:8000/](http://localhost:8000/) and the django admin
interface at [http://localhost:8000/admin/](http://localhost:8000/admin/).

Log into the admin with the credentials ``admin / admin``.

**Important:** This `docker-compose.yml` is configured for local testing only, and is _not_ intended for production use.

### Debugging
To tail the logs from the Docker containers in realtime, run:

```bash
docker-compose logs -f
```

Setup with Virtualenv
---------------------
You can run the demo locally without setting up Docker and simply use Virtualenv, which is the [recommended installation approach](https://docs.djangoproject.com/en/2.2/topics/install/#install-the-django-code) for Django itself.

#### Dependencies
* Python 3.6, 3.7 or 3.8
* [Virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
* [VirtualenvWrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) (optional)

### Installation

With [PIP](https://github.com/pypa/pip) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
installed, run:

    mkvirtualenv django_project_backup
    python --version

Confirm that this is showing a compatible version of Python 3.x. If not, and you have multiple versions of Python installed on your system, you may need to specify the appropriate version when creating the virtualenv:

    deactivate
    rmvirtualenv django_project_backup
    mkvirtualenv django_project_backup --python=python3.7
    python --version

Now we're ready to set up the sandbox demo project itself:

    cd ~/dev [or your preferred dev directory]
    git clone https://bitbucket.org/pai/django-project-backup.git
    cd django_project_backup/
    pip install -r requirements/base.txt

Next, we'll set up our local environment variables. We use [django-dotenv](https://github.com/jpadilla/django-dotenv)
to help with this. It reads environment variables located in a file name `.env` in the top level directory of the project.
The only variable we need to start is `DJANGO_SETTINGS_MODULE`:

    $ cp backend/settings/local.py.example backend/settings/local.py
    $ echo "DJANGO_SETTINGS_MODULE=backend.settings.local" > .env

To set up your database and load initial data, run the following commands:

    ./manage.py migrate
    ./manage.py load_initial_data
    ./manage.py runserver

Log into the admin with the credentials ``admin / admin``.



## Known issues

Since django-project-backup relies on natural primary keys when in **realtime** mode if one of those fields
is updated there is no efficient way to update related objects keys.



## Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
