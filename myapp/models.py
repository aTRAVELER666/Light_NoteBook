from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String,Text
from datetime import datetime
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash

from myapp.extensions import db

class User(db.Model):
    __tablename__ = 'user'
    id:Mapped[int]=mapped_column(primary_key=True)
    uid:Mapped[int]
    nickname:Mapped[str]=mapped_column(String(20))
    password_hash:Mapped[str]=mapped_column(String(128))
    space:Mapped[int]
    credit_dot:Mapped[int]
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Note(db.Model):
    __tablename__ = 'note'
    id:Mapped[int]=mapped_column(primary_key=True)
    mapped_uid:Mapped[int]
    filename:Mapped[str]=mapped_column(String(64))
    text_value:Mapped[str]=mapped_column(Text())

class Saying(db.Model):
    __tablename__ = 'saying'
    id:Mapped[int]=mapped_column(primary_key=True)
    text_value:Mapped[str]=mapped_column(Text())

class ServerData(db.Model):
    __tablename__ = 'server_data'
    id:Mapped[int]=mapped_column(primary_key=True)
    creditdot_lasttime:Mapped[datetime]
    uid_count:Mapped[int]