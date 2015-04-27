# fullstack-intro
Backup work for Udacity Full Stack Foundation course. Web Development in Python with Flask.

Preferably run in an environment with Udacity Vagrant installed.

For more info on installing the vagrant machine, check out:
https://www.udacity.com/wiki/ud088/vagrant

Either that, or you need to manually install Python 2.7.3, sqlalchemy, bleach, sqlite, flask

Once environment is setup, you can execute the server by running:
`$python server.py`

But before running the server, you need to have DB schema set up:
`python database_setup.py`

To populate the DB with some data, you can either have the `restaurantmenu.db` file 

Or, you can execute:
`python menus.py`

Finally, run the server as shown above.
