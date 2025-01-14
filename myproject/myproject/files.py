from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
import os
import random
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import pymongo
from bson import ObjectId

# Configure MongoDB connection
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['Document_Management']
coll_all_files = db['coll_all_files']

# Allowed file types for upload (to restrict unwanted file types like .exe, .bat, etc.)
ALLOWED_FILE_TYPES = ['pdf', 'jpeg', 'jpg', 'png', 'docx', 'xlsx']

# Not allowed file types (these will be restricted)
DISALLOWED_FILE_TYPES = ['exe', 'son', 'bat']

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        file_size = uploaded_file.size
        
        # Extract file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()  # Get the file extension (e.g., pdf, jpeg)

        # Check if file extension is in the allowed types list
        if file_extension not in ALLOWED_FILE_TYPES:
            # Check if the file is in the disallowed list
            if file_extension in DISALLOWED_FILE_TYPES:
                return redirect(reverse('index') + '?message=File%20type%20not%20allowed%20(safe%20restriction)%20-%20'.format(file_extension))
            return redirect(reverse('index') + '?message=File%20type%20not%20supported.%20Please%20convert%20it%20to%20a%20compatible%20format.')

        # Get additional form data (e.g., user_id, parent_folder)
        user_id = request.POST.get('user_id_file')  # Get user_id from the POST data
        parent_folder_id = request.POST.get('parent_folder')  # Get parent folder ID from the POST data
        
        # Set the base upload directory
        upload_directory_base = os.path.join(settings.BASE_DIR, 'static', 'uploads')

        # Create a subdirectory based on file type (e.g., pdf, jpeg, docx)
        upload_directory = os.path.join(upload_directory_base, file_extension)
        
        # Ensure the directory exists
        os.makedirs(upload_directory, exist_ok=True)

        # Generate new file name using the required format:
        user_id_last_digits = user_id[-4:]  # Last 4 digits of user_id_file
        random_number = random.randint(0, 999)  # Random number between 0 and 999
        current_date = datetime.now().strftime("%d%m%y")  # Current date in dd-mm-yy format
        current_time = datetime.now().strftime("%H%M%S")  # Current time in HHMMSS format

        # Create the new file name
        new_file_name = f"{user_id_last_digits}{random_number}{current_date}{current_time}.{file_extension}"

        # Handle file storage (using FileSystemStorage to save files locally)
        fs = FileSystemStorage(location=upload_directory)
        filename = fs.save(new_file_name, uploaded_file)
        
        # Construct the file URL relative to the static directory
        file_url = os.path.join('static', 'uploads', file_extension, filename)

        # Get current datetime for creation and modification
        current_date_time = datetime.now()

        # Save file data to MongoDB (coll_all_files)
        file_data = {
            'file_name': new_file_name,  # Use the newly generated file name
            'file_type': file_extension,
            'file_extension': file_extension,  # File extension based on new file name
            'is_folder': 'no',  # Mark as a file (not a folder)
            'parent_folder_name': parent_folder_id,
            'parent_folder_id': parent_folder_id,
            'location': file_url,  # Save file URL (path where it's stored)
            'user_id': user_id,
            'file_size': file_size,
            'created_on': current_date,
            'created_on_date_time': current_date_time,
            'updated_date': current_date,
            'updated_on_date_time': current_date_time
        }

        # Insert the file metadata into MongoDB
        add_file_query = coll_all_files.insert_one(file_data)
        
        if add_file_query:
            # Redirect to index page with a success message
            return redirect(reverse('index') + '?message=File%20uploaded%20successfully')
        else:
            # Redirect to index page with an error message
            return redirect(reverse('index') + '?message=Error%20uploading%20file')
    else:
        # Redirect to index page with an error message if no file is selected
        return redirect(reverse('index') + '?message=No%20file%20selected%20or%20invalid%20request')