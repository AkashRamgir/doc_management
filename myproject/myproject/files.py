from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pymongo
from datetime import datetime
import os

# MongoDB connection
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['Document_Management']
file_collection = db['coll_all_files']

# File upload logic
@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['file']  # Uploaded file
            parent_folder = request.POST.get('parent_folder', 'root')  # Parent folder name
            user_id = request.POST.get('user_id')  # User ID

            # Save file to local filesystem or a cloud storage (optional)
            save_path = f'uploads/{uploaded_file.name}'
            with open(save_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
                    
            current_date = datetime.now().strftime("%Y-%m-%d")
            current_date_time = datetime.today()

            # File metadata
            file_data = {
                'file_name': uploaded_file.name,
                'file_path': save_path,
                'file_size': uploaded_file.size,
                'file_type': uploaded_file.content_type,
                'parent_folder': parent_folder,
                'user_id': user_id,
                'created_on': datetime.now(),
                'updated_on': datetime.now()
            }
            {
                'file_name' : uploaded_file.name,
                'file_path': save_path,
                'file_type' : uploaded_file.content_type,
                'is_folder' : "no",
                'file_extension' : "",
                'parent_folder_name' : parent_folder_name,
                'parent_folder_id' : parent_folder_id,
                'location': "drive",
                'user_id' : user_id,
                'file_size' : uploaded_file.size,
                'created_on' : current_date,
                'created_on_date_time' : current_date_time,
                'updated_date' : current_date,
                'updated_on_date_time' : current_date_time
            }

            # Insert into the database
            file_collection.insert_one(file_data)

            return JsonResponse({'message': 'File uploaded successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Invalid request method'}, status=405)
