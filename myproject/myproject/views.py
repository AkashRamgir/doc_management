from django.shortcuts import render, redirect
import pymongo
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
import base64
import bcrypt
from django.contrib.auth.decorators import login_required, user_passes_test


# Configure MongoDB connection
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
mydb = client['FRA_db']
collection = mydb.tribal_data


def homepage(request):
    return render(request, "login_new.html")

def homepage_new(request):
    return render(request, "login_new.html")

def login_test(request):
   return JsonResponse(request.POST)

def index(request):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['Document_Management']
    user = request.session.get('user')  # Retrieve user from session
    parent_folder_id =request.GET.get('parent_folder')
    if parent_folder_id:
        parent_folder_id =request.GET.get('parent_folder')
    else:
        parent_folder_id ="0"
    file_collection = db['coll_all_files']
    if not user:
        return redirect('/')

    user_id = str (user['_id'])  # Convert user ID to string if necessary
    all_folders = list(file_collection.find({'user_id':  user_id,'is_folder':'yes','parent_folder_id':parent_folder_id}))  # Query files for the user
    
    # Replace _id with Id
    for folder in all_folders:
        folder['id'] = str(folder.pop('_id'))
    all_files = list(file_collection.find({'user_id':  user_id,'is_folder':'no','parent_folder_id':parent_folder_id}))  # Query files for the user


    # Return files as JSON response or render the template
    return render(request, 'index.html', {'user': user, 'user_id': user_id, 'folders': all_folders, 'files':all_files })


def about(request):
    return render(request, "about.html")


def login(request):
    return render(request,"login.html")

def logout(request):
    # Clear the user session to log out
    request.session.flush()      
    # Redirect to login page after logout
    return redirect('login')


def contact(request):
    return render(request, "contact.html")


def registration(request):
    return render(request, "registration.html")


def submit_admin_login(request):
   
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['Document_Management']
    collection = db['coll_admin']

    if request.method == 'POST':
        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Fetch all users that match the role
        users = list(collection.find({'role': role}))
        # Iterate over users and check username and password
        user_found = None
        for user in users:
            if user.get('username') == username:
                # Check if the entered password matches the hashed password
                stored_hash = user['password']  # Get the password hash from the database
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                    user_found = user
                    break
        if user_found:
            user_found['_id'] = str(user_found['_id'])  # Convert _id to string for JSON compatibility
            request.session['user'] = user_found
            if(role == "Admin"):
                return redirect('/admins/index/')
            else:
                return redirect('index')
        else:
            print("Incorrect username/password or no user found")
            return redirect('login')
    return redirect('login')

def permission_denied(request):
    return HttpResponse("Permission Denied: You do not have access to this page.", status=403)

def submit_form(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        # Get form data from request
        first_name = request.POST.get('fname')
        middle_name = request.POST.get('mname')
        last_name = request.POST.get('lname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        adhaar_card = request.FILES['adc']
        mobile_number = request.POST.get('mnumber')
        caste_certificate = request.FILES['cc']
        caste_validity = request.FILES['cv']
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        state = request.POST.get('state')
        district = request.POST.get('district')
        taluka = request.POST.get('taluka')# Convert age to integer or the appropriate data type

        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")  # Modify the connection string as needed
        db = client["FRA_db"]
        collection = db["tribal_data"]

        # Create a document (record) to insert into the collection
        data = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'dob': dob,
            'gender': gender,
            'age': age,
            'adhaar_card': adhaar_card.read(),  # Store file content as bytes
            'mobile_number': mobile_number,
            'caste_certificate': caste_certificate.read(),  # Store file content as bytes
            'caste_validity': caste_validity.read(),  # Store file content as bytes
            'address1': address1,
            'address2': address2,
            'state': state,
            'district': district,
            'taluka': taluka
            # Add more fields as needed
        }

        try:
            # Connect to MongoDB
            client = pymongo.MongoClient("mongodb://localhost:27017/")  # Modify the connection string as needed
            db = client["FRA_db"]
            collection = db["tribal_data"]

            # Insert the document into the collection
            collection.insert_one(data)

            # Close the MongoDB connection
            client.close()

            # Redirect to a success page or another page as needed
            return redirect('success')  # Modify 'success_page' to your actual success page URL

        except Exception as e:
            # Handle any exceptions that may occur during database insertion
            return HttpResponse(f"Error: {str(e)}")

    return render(request, 'index.html')


def success(request):
    return render(request, "success.html")


def retrieve_data(request):
    try:
        # Connect to MongoDB using a context manager
        with pymongo.MongoClient("mongodb://localhost:27017/") as client:
            db = client["FRA_db"]
            collection = db["tribal_data"]

            # Retrieve data from the collection (you can add query conditions if needed)
            documents = collection.find()

            # Pass the retrieved data to the template for rendering
            return render(request, 'retrieve_data.html', {'documents': documents})
    except Exception as e:
        # Handle any exceptions, for example, by returning an error response
        return HttpResponseServerError(f"An error occurred: {str(e)}")