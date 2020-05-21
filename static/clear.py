import pymongo, os, shutil
from pymongo import MongoClient
client = MongoClient()
db = client['UsersDB']
client.drop_database(db)
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ProfilesImages')
shutil.rmtree(path)
os.mkdir("ProfilesImages")