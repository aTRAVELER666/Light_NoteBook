import unittest
from http.client import responses

from app import app
from myapp import create_app
from myapp.extensions import db
from myapp.models import User,Saying,Note,ServerData

class myappTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

        user1 = User(nickname="paimon")
        user1.set_password('123')
        user2 = User(nickname="traveler")
        user2.set_password('paimon')
        saying1=Saying(text_value="Hello World!")
        saying2=Saying(text_value="Wake Up!")
        saying3=Saying(text_value="Hi,traveler.")
        server_data=ServerData(uid_counter=0)
        server_data.register_user(user1)
        server_data.register_user(user2)
        user1.add_text("My tmp text.md","# Hello World!")
        user2.add_text("我与飞鸟","鸟为什么会飞？")
        db.session.add_all([user1,user2,saying1,saying2,saying3,server_data])
        db.session.commit()

        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()
    def test_app_exists(self):
        self.assertIsNotNone(self.app)
    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])
    def test_index_page(self):
        response = self.client.get("/")