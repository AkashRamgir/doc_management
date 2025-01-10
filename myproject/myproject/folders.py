from django.shortcuts import render, redirect
import pymongo
from django.http import HttpResponse, HttpResponseServerError,JsonResponse
import base64
from datetime import date, datetime
from bson.objectid import ObjectId

# Configure MongoDB connection
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['Document_Management']
# collection = db['coll_admin']

def create_new_folder(request):
    folder_collection = db['coll_folders']
    coll_all_files = db['coll_all_files']
    folder_name = request.POST.get('folder_name')
    parent_folder_id = request.POST.get('parent_folder')
    user_id = request.POST.get('user_id')
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_date_time = datetime.today()
    if parent_folder_id != "0":
        parent_folder = folder_collection.find_one({'_id': ObjectId(parent_folder_id)})
        parent_folder_name = parent_folder['folder_name'] if parent_folder else None
    else:
        parent_folder_name = "root"
    
    if(request.method == "POST"):
        folder_data = {
            'folder_name': folder_name,
            'parent_folder_name' : parent_folder_id,
            'parent_folder_id' : parent_folder_name,
            'user_id' : user_id,
            'created_on' : current_date,
            'created_on_date_time' : current_date_time,
            'updated_date' : current_date,
            'updated_on_date_time' : current_date_time
        }
        add_folder_query = folder_collection.insert_one(folder_data)
        if(add_folder_query):
            inserted_id = add_folder_query.inserted_id
            file_coll_data = {
                'file_name' : folder_name,
                'file_type' : "folder",
                'is_folder' : "yes",
                'file_extension' : "",
                'parent_folder_name' : parent_folder_name,
                'parent_folder_id' : parent_folder_id,
                'location': "drive",
                'user_id' : user_id,
                'file_size' : '',
                'created_on' : current_date,
                'created_on_date_time' : current_date_time,
                'updated_date' : current_date,
                'updated_on_date_time' : current_date_time
                
            }
            add_file_query = coll_all_files.insert_one(file_coll_data)
            if(add_file_query):
                msg = {'message': "Success",'msg' : 'Folder created succesfully!!'}
            msg = {'message': "Success",'inserted_id': str(add_folder_query.inserted_id)}
        else:
            msg = {'message': "Error"}
    return JsonResponse(msg)
