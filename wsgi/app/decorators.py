#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 - fxlovely <fxlovely@outlook.com>

from functools import wraps
from flask_login import current_user
from flask import abort

def admin_required(f):
    @wraps(f)
    def decorator_admin(*args, **kwargs):
        if current_user.Role_id == 7 or current_user.Role_id == 9:
            return f(*args, **kwargs)
        else:
            abort(403)
    return decorator_admin

def super_admin_required(f):
    @wraps(f)
    def decorator_superadmin(*args, **kwargs):
        if current_user.Role_id == 9:
            return f(*args, **kwargs)
        else:
            abort(403)
    return decorator_superadmin
