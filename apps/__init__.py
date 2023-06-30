# -*- coding: utf-8 -*
# @Time    : 2023/6/25 14:11
# @Author  : liuy
# @File    : __init__.py.py

from flask import Flask
from apps.views.view import view_bule


app = Flask(__name__)
app.register_blueprint(view_bule)

