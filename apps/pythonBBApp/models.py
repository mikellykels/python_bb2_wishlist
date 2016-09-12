from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def login(self, **kwargs):
        if kwargs is not None:
            errors = {}
            if len(kwargs['password']) == 0:
                errors['password'] = "Please Enter a Password"
            if len(kwargs['username']) == 0:
                errors['username'] = "Please Enter an Username"
            if len(errors) != 0:
                return (False, errors)
            else:
                user = User.userMgr.filter(username=kwargs['username'])
                if not user:
                    errors['user'] = "Email/Password Combination Not Found"
                    return (False, errors)
                else:
                    if bcrypt.checkpw(kwargs['password'].encode('utf-8'), user[0].password.encode('utf-8')):
                        return (True, user[0])
                    else:
                        errors['user'] = "Email/Password Combination Not Found"
                        return (False, errors)

    def register(self, **kwargs):
        if kwargs is not None:
            errors = {}
            if len(kwargs['name']) < 2:
                errors['name'] = "Name must be at least 2 characters"
            if len(kwargs['username']) < 2:
                errors['username'] = "Username must be at least 2 characters"
            if len(kwargs['email']) == 0:
                errors['email'] = "Email is required"
            elif not EMAIL_REGEX.match(kwargs['email']):
                errors['email'] = "Please enter a valid email"
            if len(kwargs['password']) < 8:
                errors['password'] = "Password must be at least 8 characters"
            if kwargs['password'] != kwargs['confirm_pw']:
                errors['confirm_pw'] = "Passwords must match"
            if len(errors) is not 0:
                return (False, errors)
            else:
                hashed = bcrypt.hashpw(kwargs['password'].encode('utf-8'), bcrypt.gensalt())
                user = User.userMgr.create(name=kwargs['name'], username=kwargs['username'], email=kwargs['email'], password=hashed)
                user.save()
                return (True, user)
        else:
            messages.add_message(request, messages.INFO, "Please Try Registration Again")
            return (False, user)

class User(models.Model):
    name       = models.CharField(max_length=200)
    username   = models.CharField(max_length=200)
    email      = models.EmailField(max_length=45)
    password   = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userMgr    = UserManager()

class WishListManager(models.Manager):
    def add(self, **kwargs):
        if kwargs is not None:
            errors = {}
            if len(kwargs['item']) < 2:
                errors['item'] = "Item must be at least 2 characters"
            if len(errors) is not 0:
                return (False, errors)
            else:
                u = User.userMgr.get(
                    id    = kwargs['user']
                    )
                w = WishList.wishListMgr.create(
                    user  = u,
                    item  = kwargs['item']
                    )
                return (True, w)

class WishList(models.Model):
    user        = models.ForeignKey(User, related_name='user_id')
    item        = models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    wishListMgr = WishListManager()
