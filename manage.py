#!/usr/bin/env python
import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db
from app.location import location_refresh
from app.models import Truck, User


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Truck=Truck, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def deploy():
    """Run deployment tasks"""
    from flask.ext.migrate import upgrade
    # migrate database to latest revision
    upgrade()


@manager.command
def refresh_twitter_info():
    """Refresh truck twitter fields (last tweet, thumbnail, etc.)"""
    Truck.twitter_refresh()


@manager.command
def refresh_truck_locations():
    """Refresh truck location fields"""
    location_refresh()


if __name__ == '__main__':
    manager.run()
