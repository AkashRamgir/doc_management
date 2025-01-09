from django.shortcuts import render, redirect
import pymongo
from django.http import HttpResponse, HttpResponseServerError,JsonResponse
import base64

# Configure MongoDB connection
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['Document_Management']
# collection = db['coll_admin']

def create_new_folder(request):
    folder_collection = db['coll_folders']
    coll_all_files = db['coll_all_files']
    folder_name = request.POST.get('folder_name')
    parent_folder_name = request.POST.get('parent_folder')
    user_id = request.POST.get('user_id')
    if(request.method == "POST"):
        folder_data = {
            'folder_name': folder_name,
            'parent_folder' : parent_folder_name,
            'user_id' : user_id
        }
        # folder_collection.insert_one(folder_data)
    return JsonResponse({'message':folder_data})
