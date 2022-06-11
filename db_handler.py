import pyrebase
import json

class DBmodule:
    def __init__(self):
        with open("./auth/auth.json") as f:
            config = json.load(f)

        self.firebase = pyrebase.initialize_app(config)

    def login(self, id, pw):
        pass

    def signin(self, id, pw, name):
        pass     

    def write_post(self, user, contents):
        pass

    def post_list(self):
        pass

    def post_detail(self, pid):
        pass

    def get_user(self, uid):
        pass
