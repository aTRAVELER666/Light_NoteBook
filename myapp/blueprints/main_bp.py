from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from sqlalchemy import select

from myapp.models import User,Note,Saying,ServerData
from myapp.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
@main_bp.route('/home', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main_bp.route('/editor', methods=['GET', 'POST'])
def editor():
    return render_template('editor.html')

@main_bp.route("/reader",methods=['GET', 'POST'])
def reader():
    return render_template('reader.html')