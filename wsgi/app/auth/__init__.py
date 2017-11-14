#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 - fxlovely <fxlovely@outlook.com>

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
