from xmlrpc.client import DateTime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Text, select
from datetime import datetime
from sqlalchemy.orm import Mapped,mapped_column,DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user,UserMixin

from myapp.extensions import db

space_limit=20971520

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id:Mapped[int]=mapped_column(primary_key=True)
    uid:Mapped[int]
    username:Mapped[str]=mapped_column(String(20))
    nickname:Mapped[str]=mapped_column(String(20))
    password_hash:Mapped[str|None]=mapped_column(String(128))
    space:Mapped[int] #使用存储空间，单位字节(Byte)
    credit_dot:Mapped[int]
    last_login_time:Mapped[datetime]=mapped_column(default=datetime.now())
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
    def calc_add(self,length):
        if self.space > space_limit:
            return "space error"
        if self.credit_dot-length<-1048576 or self.credit_dot<0:
            return "credit dot error"
        self.space += length
        self.credit_dot -= length
        return "success"
    def add_note(self,filename,text_value):
        note=db.session.execute(select(Note).filter_by(mapped_uid=self.uid,filename=filename)).scalar()
        length=len(str(text_value))
        calc_answer=self.calc_add(length)
        if calc_answer=="space error":
            return "space error"
        elif calc_answer=="credit dot error":
            return "credit dot error"
        if note:
            return "note already exists"
        else :
            note=Note(mapped_uid=self.uid,filename=filename,text_value=text_value,text_size=length)
            db.session.add(note)
            db.session.commit()
            self.space += length
            self.credit_dot -= length
            return "success"
    def remove_note(self,filename):
        note=db.session.execute(select(Note).filter_by(mapped_uid=self.uid,filename=filename)).scalar()
        if note:
            self.space-=note.text_size
            db.session.delete(note)
            db.session.commit()
            return "success"
        else:
            return "note not found"
    def rename_note(self,filename,new_filename):
        note=db.session.execute(select(Note).filter_by(mapped_uid=self.uid,filename=filename)).scalar()
        if not note:
            return "note not found"
        new_note=db.session.execute(select(Note).filter_by(mapped_uid=self.uid,filename=new_filename)).scalar()
        if new_note:
            return "new notename already exists"
        else:
            note.filename=new_filename
            return "success"
    def write_note(self,filename,text_value):
        note=db.session.execute(select(Note).filter_by(mapped_uid=self.uid,filename=filename)).scalar()
        if not note:
            return "note not found"
        length=len(str(text_value))
        calc_answer=self.calc_add(length)
        if calc_answer=="space error":
            return "space error"
        elif calc_answer=="credit dot error":
            return "credit dot error"
        note.text_value=text_value
        note.text_size=length
        db.session.commit()

    def read_note(self,filename):
        note=db.session.execute(select(Note).filter_by(mapped_uid=self.uid,filename=filename)).scalar()
        if note:
            return note.text_value
        else:
            return ""
    def search_note(self):
        note=db.session.execute(select(Note).filter_by(mapped_uid=self.uid)).scalars().all()
        return note

class Note(db.Model):
    __tablename__ = 'note'
    id:Mapped[int]=mapped_column(primary_key=True)
    mapped_uid:Mapped[int]
    filename:Mapped[str]=mapped_column(String(64))
    text_value:Mapped[str]=mapped_column(Text())
    text_size:Mapped[int]

class Saying(db.Model):
    __tablename__ = 'saying'
    id:Mapped[int]=mapped_column(primary_key=True)
    text_value:Mapped[str]=mapped_column(Text())

class ServerData(db.Model):
    __tablename__ = 'server_data'
    id:Mapped[int]=mapped_column(primary_key=True)
    uid_counter:Mapped[int]
    def register_user(self,username,nickname,password):
        if self.uid_counter>=1000:
            return {"status":"Have no more uids","user":None}
        user=db.session.execute(select(User).filter_by(username=username)).scalar()
        if user is not None:
            return {"status":"User already exists","user":None}
        user=User(username=username,nickname=nickname,uid=self.uid_counter+1000,
                    space=0,credit_dot=52428800)
        user.set_password(password)
        self.uid_counter+=1
        db.session.add(user)
        db.session.commit()
        return {"status":"User registered","user":
                db.session.execute(select(User).filter_by(username=username)).scalar() }
