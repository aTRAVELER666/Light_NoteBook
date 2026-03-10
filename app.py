from flask import Flask, render_template
from markupsafe import escape
import unittest
import os
import sys
import datetime
app = Flask(__name__)
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template("basic_page.html")