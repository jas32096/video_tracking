Tested with
  Python 3.6.2
  PostgreSQL 9.6.4

Environment
  If you'd like, create a virtual env for this project
    $ python3 -m venv .env
    $ source .env/bin/activate
  Install dependencies
    $ pip install -r requirements.txt

Database
  I used Postgres. If you'd like to use a different DB make sure to add the proper dependencies
  and update SQLALCHEMY_DATABASE_URI in config.py.

  You can create the DB with the SQL from create.sql or create a database called g9_video_dev
  and run db.create_all() in a python shell.
  >>> from app import db
  >>> db.create_all()

To Run
  $ python run.py

  This will create the application, in debug mode, on localhost:5000

  IMPORANT Note: In production you'd want to put the app behind a proper WSGI.
                 +===============================+
                 |DON'T USE run.py IN PRODUCTION!|
                 +===============================+
