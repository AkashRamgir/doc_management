from django.shortcuts import render, redirect
import pymongo
from django.http import HttpResponse, HttpResponseServerError
from django.http import JsonResponse
import os
import bcrypt
from django.conf import settings
import base64

# Configure MongoDB connection
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['Document_Management']
collection = db['coll_admin']


def add_users(request):    
        # for fetching the users
        users = list(collection.find({'role': 'User'}))  # Fetch users with role 'User'
        user = request.session.get('user')      
        return render(request, "add_users.html", {'user_role': users, 'user_id': user['_id']})

def save_users(request):
    if request.method == "POST":
        # Retrieve form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')
        profile_photo = request.FILES.get('profile_photo')  # Retrieve uploaded file

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Define the path to store profile photos
        upload_dir = os.path.join(settings.BASE_DIR, 'static', 'assets', 'profile_photos')

        # Ensure the directory exists
        os.makedirs(upload_dir, exist_ok=True)

        # Initialize photo path
        photo_path = '/static/assets/profile_photos/default.jpg'  # Default photo path

        # Save the uploaded file
        if profile_photo:
            try:
                # Use a unique filename to avoid overwriting
                file_name = f"{username}_{profile_photo.name}"
                # print("file path is", file_name)
                # return
                file_path = os.path.join(upload_dir, file_name)
                # print("file path is", file_name)
                # return
                # Save file to the directory
                with open(file_path, 'wb+') as destination:
                    for chunk in profile_photo.chunks():
                        destination.write(chunk)

                # Set the relative photo path
                photo_path = f'/static/assets/profile_photos/{file_name}'

                # Debugging output
                print(f"File saved at: {file_path}")           

            except Exception as e:
                print(f"Error saving file: {e}")
                return JsonResponse({'status': 'error', 'message': f'Error saving file: {e}'})
            
            # Save to the database
            try:
                collection.insert_one({
                    'username': username,
                    'email': email,
                    'password': hashed_password,  # Save hashed password
                    'role': role,
                    'applicant_photo': photo_path
                })

                # Debugging output
                print(f"User added successfully: {username}")
            except Exception as e:
                print(f"Error saving to database: {e}")
                return JsonResponse({'status': 'error', 'message': f'Error saving to database: {e}'})
       

        # Return a success response
        return JsonResponse({'status': 'success', 'message': 'User added successfully!'})

    # If not a POST request, return an error response
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def update_user(request, user_id):
    return HttpResponse( user_id)