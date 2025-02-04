from django.shortcuts import render, redirect
import pymongo
from django.http import HttpResponse, HttpResponseServerError,JsonResponse
import base64
from datetime import date, datetime
from bson.objectid import ObjectId
# Configure MongoDB connection
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['Document_Management']
def dashboard(request):
    return render(request, "admin/dashbard.html")

def user_list(request):
    collection = db['coll_admin']
    # for fetching the users
    users = list(collection.find({'role': 'User'}))  # Fetch users with role 'User'
    # user = request.session.get('user')              
    for u in users:
        u['id'] = str(u.pop('_id'))
    return render(request, "admin/user_list.html", {'user_role': users})


