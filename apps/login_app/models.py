from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if len(postData['fName']) < 2:
            errors["name"] = "Name has to be more than 5 characters"
        print len(postData['lName'])
        if len(postData['lName']) < 2:
            errors['desc'] = "Description has to be more than 10 characters"
        if len(postData['email']) >2:
            try:
                validate_email(postData['email'])
            except ValidationError as e:
                errors['email']="Wrong Email"
        if len(postData['password']) < 8:
            errors["name"] = "Password has to be more than 8 characters"
        if len(postData['cpassword']) < 8:
            errors['desc'] = "Password confirmation has to be more than 10 characters"
        if postData['password']!=postData['cpassword']:
            errors['password']="Password confirmation does not match Password"
        
        return errors

class Users(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email_address=models.CharField(max_length=45)
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __repr__(self):
        return "<Object name{},lastname {},email{}>".format(self.first_name,self.last_name,self.email_address)

    objects=UserManager()

