from django.shortcuts import render, redirect
from .models import *
from django.apps import apps
User = apps.get_model('login_app', 'User')

# Create your views here.
def index(request):
    context = {
        'messages': Message.objects.all()
    }
    return render(request, 'wall_index.html', context)

def new_message(request):
    this_user= User.objects.get(id=request.session['user_id']) 
    new_message= Message.objects.create(message= request.POST['message'], user=this_user)
    return redirect('/wall')

def post_comment(request, message_id):
    this_message = Message.objects.get(id=message_id)
    another_user= User.objects.get(id=request.session['user_id'])
    new_comment= Comment.objects.create(comment= request.POST['comment'], user= another_user, message= this_message)
    return redirect('/wall')