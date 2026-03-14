from myapp.extensions import db
from myapp.models import ServerData,Saying,User,Note
import click

from myapp.models import ServerData, Saying


def build_database():
    server_data = ServerData(uid_counter=0)
    user1=server_data.register_user("test user1","paimon","123")["user"]
    user2=server_data.register_user("test user2","traveler","123456")["user"]
    saying1=Saying(text_value="test saying1")
    saying2=Saying(text_value="test saying2")
    saying3=Saying(text_value="test saying3")
    user1.add_note("my teMp text.md","<hello world>")
    user2.add_note("我与飞鸟","鸟为什么会飞")
    db.session.add_all([saying1,saying2,saying3,server_data])
    db.session.commit()

def register_commands(app):
    @app.cli.command()
    def forge():
        db.drop_all()
        db.create_all()
        build_database()
        click.echo('Done.')

    @app.cli.command("init-db")
    @click.option("--drop",is_flag=True,help="Create after drop.")
    def init_database(drop):
        if drop:
            db.drop_all()
        db.create_all()
        click.echo('Initialized database.')