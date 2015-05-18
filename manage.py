#!/usr/bin/env python2
from flask.ext.script import Manager

from web2lp import app

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
