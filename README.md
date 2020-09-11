# Component Manager

Currently broken due to not using fixed versions for dependencies.
(means: still runs on my old system, but not when newly set up.)

- create a virtual environment and activate it
``` bash
virtualenv venv
source ./venv/bin/activate
```
- install dependencies
``` bash
pip install -r requirements.txt
```

- setup a MySQL database. Add your URL and credentials in `settings.py`

- setup the database tables using
``` BASH
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

- start the server
``` BASH
python manage.py runserver
```

