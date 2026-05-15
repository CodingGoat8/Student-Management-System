

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["school"]

student_collection = db["students"]

user_collection = db["users"]






