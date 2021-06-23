from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        users = User.objects.filter(email = postData['email'])
        if len(users) > 0:
            errors['email_used'] = "E-mail already in use"
        if len(postData['first_name']) <2:
            errors['first_name'] = "First name should be at least 2 characters"
        first_name_REGEX = re.compile(r'^[a-zA-Z]+$')
        if not first_name_REGEX.match(postData['first_name']):           
            errors['first_name'] = ("Invalid first name!")
        if len(postData['last_name']) <2:
            errors['last_name'] = "Last name should be at least 2 characters"
        last_name_REGEX = re.compile(r'^[a-zA-Z]+$')
        if not last_name_REGEX.match(postData['last_name']):           
            errors['last_name'] = "Invalid last name!"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(postData['password']) <8:
            errors['password'] = 'Password should be at least 8 characters'
        if postData['confirm'] != postData['password']:
            errors['confirm'] = 'Passwords do not match'
        return errors


class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.CharField(max_length=45)
    password= models.CharField(max_length=65)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()
