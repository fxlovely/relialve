#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 - fxlovely <fxlovely@outlook.com>

import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

'''
app = create_app()
relialve = Manager(app)
migrate = Migrate(app, db)

relialve.add_command('db', MigrateCommand)
'''

relialve = create_app()

if __name__ == '__main__':
    relialve.run()
