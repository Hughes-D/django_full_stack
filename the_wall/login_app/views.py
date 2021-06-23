from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create(request):
    errors = User.objects.user_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
                first_name=request.POST['first_name'], 
                last_name=request.POST['last_name'], 
                email= request.POST['email'], 
                password=pw_hash
        )
        messages.success(request, "User successfully created")
        request.session['user_id'] = new_user.id
        return redirect('/wall')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    one_user= User.objects.get(id=request.session['user_id'])
    context = {
        'user_first_name': one_user.first_name
    }
    return render(request, 'welcome.html', context)

def login(request):
    users = User.objects.filter(email = request.POST['email'])
    if len(users) == 0:
        messages.error(request, "User doesn't exsits")
        return redirect('/')
    user= users[0]
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        print("password match")
        request.session['user_id'] = user.id
        return redirect('/wall')
    else:
        print("failed password")
        messages.error(request, "Wrong password")
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')