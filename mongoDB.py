from transformers import TFAlbertForSequenceClassification

students = [
    {"student_id": "S101", "name": "Anya Patel",  "email": "anya.patel@campus.edu",   "major": "Computer Science"},
    {"student_id": "S102", "name": "Jordan Lee",  "email": "jordan.lee@campus.edu",   "major": "Mechanical Engineering"},
    {"student_id": "S103", "name": "Fatima Khan", "email": "fatima.khan@campus.edu",  "major": "Electrical Engineering"},
    {"student_id": "S104", "name": "Leo Hernandez","email": "leo.hernandez@campus.edu","major": "Computer Science"},
]

courses = [
    {"course_id": "C201", "title": "Software Architecture", "instructor": "Dr. Alice Chen", "credits": 4},
    {"course_id": "C202", "title": "Thermodynamics",        "instructor": "Prof. John Miller", "credits": 3},
    {"course_id": "C203", "title": "AI Systems",            "instructor": "Dr. Nina Singh", "credits": 4},
    {"course_id": "C204", "title": "Circuit Analysis",      "instructor": "Dr. Ravi Patel", "credits": 3},
]

rooms = [
    {"room_id": "R301", "building": "Engineering Block A", "capacity": 50, "nowStudent":0, "isReserved":0},
    {"room_id": "R302", "building": "Science Center",      "capacity": 40, "nowStudent":0, "isReserved":0},
    {"room_id": "R303", "building": "Innovation Hub",      "capacity": 60, "nowStudent":0, "isReserved":0},
]

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI',"mongodb://localhost:27017/")

client = MongoClient(MONGO_URI)

db=MONGO_DB = os.getenv('MONGO_BD',"New_DB")

#def new_db(db_name):
#
 #   global db
 #   db = client[MONGO_DB]

def init_db():
    db.students.create_index("student_id", unique=True)
    for student in students:
        db.students.update_one(
            {"student_id": student["student_id"]},
            {"$set": student},
            upsert=True,
        )

    db.courses.create_index("course_id", unique=True)
    for course in courses:
        db.courses.update_one(
            {"course_id": course["course_id"]},
            {"$set": course},
            upsert=True,
        )

    db.rooms.create_index("room_id", unique=True)
    for room in rooms:
        db.rooms.update_one(
            {"room_id": room["room_id"]},
            {"$set": room},
            upsert=True,
        )

def get_room_by_id(room_id):
    room=db.read_rooms.find_one({"room_id": room_id})
    return room

def room_reserve(room_id):
    room = db.read_rooms.find_one({"room_id": room_id})
    if room is None:
        return False
    if room["isReserved"]==1:
        return False
    room["isReserved"]=0
    db.rooms.update_one(
        {"room_id": room_id},
        {"$set": room},
        upsert=True,
    )
    return True

