from django.shortcuts import render, redirect
import pymongo
from django.http import HttpResponse, HttpResponseServerError
from django.http import JsonResponse
import os
import bcrypt
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
import base64
from django.contrib.auth.models import User
from django.contrib import messages
from bson import ObjectId
from datetime import datetime
from django.contrib.auth.decorators import login_required 

# Configure MongoDB connection
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['Document_Management']
collection = db['coll_admin']


def add_users(request):    
        # for fetching the users
        users = list(collection.find({'role': 'User'}))  # Fetch users with role 'User'
        # user = request.session.get('user')              
        for u in users:
            u['id'] = str(u.pop('_id'))
        return render(request, "add_users.html", {'user_role': users} )


def save_users(request):
    if request.method == "POST":
        # Retrieve form data
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')
        profile_photo = request.FILES.get('profile_photo')  # Retrieve uploaded file
        created_at =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')        
        users = request.session.get('user')         
        if users and '_id' in users:
            logged_in_userId = str(users['_id'])  # Convert `_id` to string
            print("Logged-in User ID:", logged_in_userId)
        else:
            print("User data not found in session")
          
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
                file_path = os.path.join(upload_dir, file_name)               
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
                    'full_name' : full_name,
                    'username': username,
                    'email': email,
                    'password': hashed_password,  # Save hashed password
                    'hashedPassword': password,
                    'role': role,
                    'applicant_photo': photo_path,
                    'created_at': created_at,
                    'created_by':logged_in_userId
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




def get_user(request):
    try:
        if request.method == "POST":
            user_id = request.POST.get('userId')

            # Check if user_id is missing
            if not user_id:
                return JsonResponse({'error': 'User ID is missing'}, status=400)

            # Convert the user_id to ObjectId (MongoDB format)
            try:
                object_id = ObjectId(user_id)
            except Exception as e:
                return JsonResponse({'error': f'Invalid ObjectId format: {str(e)}'}, status=400)

            # Query the MongoDB collection to find the user by _id
            user = collection.find_one({'_id': object_id})
            print("User", user)

            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)

            # Return the user information in the response
            return JsonResponse({
                'id': str(user['_id']),  # Convert ObjectId to string for the response
                'fullname': user.get('full_name'),
                'username': user.get('username'),
                'email': user.get('email'),
                'role': user.get('role')  # Adjust according to your document fields               
            })

        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)

    except Exception as e:
        # Catch any unexpected errors and return a response
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


def update_user(request):
    users = request.session.get('user')         
    if users and '_id' in users:
            logged_in_userId = str(users['_id']) 
    
    if request.method == 'POST':
        try:
            # Get the user ID from the form
            user_id = request.POST.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'User ID is missing'}, status=400)

            # Convert the user_id to an ObjectId
            object_id = ObjectId(user_id)
        except Exception as e:
            return JsonResponse({'error': f'Invalid ObjectId format: {str(e)}'}, status=400)

        user = collection.find_one({'_id': object_id})
        # user = get_object_or_404(User, id=user_id)  # Get the user by the ID
        
        # Get the data from the POST request
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')  # Make sure this field is populated in your form
        updated_at =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')   
        
      # Prepare the update query
        update_fields = {}
        if full_name:
            update_fields['full_name'] = full_name
        if username:
            update_fields['username'] = username
        if email:
            update_fields['email'] = email
        if role:
            update_fields['role'] = role
        update_fields['updated_at']= updated_at
        update_fields['updated_by']=logged_in_userId

        # Update the user in the MongoDB collection
        result = collection.update_one({'_id': object_id}, {'$set': update_fields})
        if result.modified_count == 0:
            return JsonResponse({'status': 'warning', 'message': 'No changes were made.'})

        # Return a success response
        return JsonResponse({
            'status': 'success',
            'message': 'User updated successfully.'
        })

    # If the method is not POST, return an error
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def delete_user(request):
    if request.method == 'POST':
        try:
            # Extract user ID from the POST request
            user_id = request.POST.get('user_id')
            if not user_id:
                return JsonResponse({'status': 'error', 'message': 'User ID is required'}, status=400)

            # Convert the user ID to an ObjectId
            object_id = ObjectId(user_id)

            # Delete the user from the database
            result = collection.delete_one({'_id': object_id})

            if result.deleted_count == 1:
                return JsonResponse({'status': 'success', 'message': 'User deleted successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
