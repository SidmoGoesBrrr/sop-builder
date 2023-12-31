from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import streamlit as st
import pytz
# Connect to MongoDB
client = MongoClient(
    st.secrets["db_url"]
)
db = client["SOP_Builder"]
users_collection = db["users"]
login_collection = db["logins"]
# User Schema
user_schema = {
    "username": "",
    "email": "",
    "phone_number": "",
    "last_logged_in": None,
    "program": "",
    "university": "",
    "field_interest": "",
    "career_goal": "",
    "subjects_studied": "",
    "projects_internships": "",
    "lacking_skills": "",
    "program_benefits": "",
    "contribution": "",
    "conclusion": "",
    "SOP_CREDITS": 0,
    "drafts": []
}


# Functions for CRUD operations for users


def create_user(username, email, phone_number):
    user_data = user_schema.copy()
    user_data["username"] = username
    user_data["email"] = email
    user_data["phone_number"] = phone_number
    ist = pytz.timezone('Asia/Kolkata')
    user_data["last_logged_in"] = datetime.now(ist).strftime("%A,%d %B %Y - %H:%M:%S")
    result = users_collection.insert_one(user_data)
    return result.inserted_id


def get_user_data(username):
    return users_collection.find_one({"username": username})


def get_user_data_by_id(id):
    objInstance = ObjectId(id)
    return users_collection.find_one({"_id": objInstance})


def update_user(username, data):
    users_collection.update_one({"username": username}, {"$set": data})


def update_user_by_id(id,data):
    objInstance = ObjectId(id)
    users_collection.update_one({"_id": objInstance}, {"$set": data})


def delete_user(username):
    result = users_collection.delete_one({"username": username})
    return result.deleted_count

def delete_user_by_id(id):
    objInstance = ObjectId(id)
    result = users_collection.delete_one({"_id": objInstance})
    return result.deleted_count
# Functions for CRUD operations for login
