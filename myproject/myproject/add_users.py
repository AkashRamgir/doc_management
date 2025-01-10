from django.shortcuts import render, redirect
import pymongo
from django.http import HttpResponse, HttpResponseServerError
import base64

# Configure MongoDB connection
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['Document_Management']
collection = db['coll_admin']


def add_users(request):
    users = list(collection.find({'role': 'User'}))  # Fetch users with role 'User'
    user = request.session.get('user')
    # user_id= 
    return render(request, "add_users.html", {'user_role': users, 'user_id': user['_id']})

def update_user(request, user_id):
    return HttpResponse( user_id)