

from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://codinggoat8_db_user:SMS_69@sms.bjexqul.mongodb.net/?retryWrites=true&w=majority&appName=SMS"
)

db = client["school"]

student_collection = db["students"]

user_collection = db["users"]






