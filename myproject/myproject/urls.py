"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views, folders, users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('submit_admin_login/', views.submit_admin_login, name='submit_admin_login'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('registration/', views.registration, name='registration'),
    path('submit_form/', views.submit_form, name='submit_form'),
    path('success/', views.success, name='success'),
    path('retrieve_data/', views.retrieve_data, name='retrieve_data'),
    path('create_folder/', folders.create_new_folder, name='create_folder'),

    # Add User Functionality in Admin
    path('users/', users.add_users, name='add_users'),
    path('save_users/', users.save_users, name='save_users'),
    path('get_user/', users.get_user, name='get_user'),
    path('update_user/', users.update_user, name='update_user'),
    path('delete_user/', users.delete_user, name='delete_user'),
]
