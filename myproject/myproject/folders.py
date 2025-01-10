from django.shortcuts import render, redirect
import pymongo
from django.http import HttpResponse, HttpResponseServerError,JsonResponse
import base64
from datetime import date, datetime

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
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_date_time = datetime.today()
    if(request.method == "POST"):
        folder_data = {
            'folder_name': folder_name,
            'parent_folder' : parent_folder_name,
            'user_id' : user_id,
            'created_on' : current_date,
            'created_on_date_time' : current_date_time,
            'updated_date' : current_date,
            'updated_on' : current_date_time
        }
        add_folder_query = folder_collection.insert_one(folder_data)
        if(add_folder_query):
            inserted_id = add_folder_query.inserted_id
            file_coll_data = {
                
            }
            # msg = {'message': "Success",'inserted_id': str(add_folder_query.inserted_id)}
        else:
            msg = {'message': "Error"}
    return JsonResponse(msg)
