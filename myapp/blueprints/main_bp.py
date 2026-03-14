import datetime
import random
from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy import select

from myapp.models import User,Note,Saying,ServerData
from myapp.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
@main_bp.route('/home', methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated:
        return render_template('index.html',username="",nickname="",notes=[])
    if request.method == 'POST':
        filename=request.form.get('filename')
        text_value=request.form.get('text_value')
        current_user.add_note(filename,text_value)
        return redirect(url_for('main.index'))
    notes=current_user.search_note()
    sayings=db.session.execute(select(Saying)).scalars().all()
    saying=sayings[random.randint(0,len(sayings)-1)].text_value
    return render_template('index.html',notes=notes,saying=saying)

@main_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('settings.html')

@main_bp.route('/editor/<filename>', methods=['GET', 'POST'])
def editor(filename):
    if request.method == 'POST':
        current_user.write_note(filename,request.form.get('text_value'))
        flash("success")
        return redirect(url_for('main.index'))
    note=db.session.execute(select(Note).filter_by(mapped_uid=current_user.uid,filename=filename)).scalar().text_value
    return render_template('editor.html',note=note)

@main_bp.route("/reader/<int:note_id>",methods=['GET', 'POST'])
def reader(note_id):
    note = db.get_or_404(Note, note_id)
    return render_template('reader.html',note=note.text_value)

@main_bp.route("/delete/<filename>",methods=['GET', 'POST'])
@login_required
def deleter(filename):
    current_user.remove_note(filename)
    return redirect(url_for('main.index'))

@main_bp.route("/login",methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        uid = request.form.get('uid')
        password = request.form.get('password')
        if (not username and not uid) or (not password):
            flash("Invalid input.")
            return redirect(url_for('main.login'))
        if username:
            user=db.session.execute(select(User).filter_by(username=username)).scalar()
        else :
            user=db.session.execute(select(User).filter_by(uid=uid)).scalar()
        if user is not None and user.validate_password(password):
            login_user(user)
            flash("Login successful.")
            return redirect(url_for('main.index'))
        flash("Login failed.")
    return render_template('login.html')

@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Goodbye.")
    return redirect(url_for('main.index'))

@main_bp.route("/register",methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        repeat = request.form.get('repeat')
        if (not username) or (not password) or (not repeat):
            flash("Invalid input.")
            return redirect(url_for('main.register'))
        if password != repeat:
            flash("Passwords don't match.")
            return redirect(url_for('main.register'))
        if not nickname:
            nickname = username
        server_data = db.session.execute(select(ServerData)).scalar()
        server_data.register_user(username,nickname,password)
        return redirect(url_for('main.index'))
    return render_template('register.html')