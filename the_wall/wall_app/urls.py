from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new_message', views.new_message),
    path('post_comment/<int:message_id>', views.post_comment),

]
