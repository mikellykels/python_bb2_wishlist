from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *

# Create your views here.

def index(request):
    return render(request, 'pythonBBApp/index.html')

def register(request):
    if request.method == "POST":
        result = User.userMgr.register(
            name        =   request.POST['name'],
            username    =   request.POST['username'],
            email       =   request.POST['email'],
            password    =   request.POST['password'],
            confirm_pw  =   request.POST['confirm_pw']
        )
        if result[0]:
            request.session['user_id'] = result[1].id
            request.session['user_name'] = result[1].name
            return redirect(reverse('dashboard'))
        else:
            for error in result[1]:
                messages.add_message(request, messages.INFO, result[1][error])
            return redirect(reverse('index'))
    else:
        return redirect(reverse('index'))

def login(request):
    if request.method == "POST":
        result = User.userMgr.login(
            username    =   request.POST['username'],
            password    =   request.POST['password']
        )
        if result[0]:
            request.session['user_id'] = result[1].id
            request.session['user_name'] = result[1].name
            return redirect(reverse('dashboard'))
        else:
            for error in result[1]:
                messages.add_message(request, messages.INFO, result[1][error])
            return redirect(reverse('index'))
    else:
        return redirect(reverse('index'))

def dashboard(request):
    wishlist = WishList.wishListMgr.all()

    user_object = User.userMgr.get(id=request.session['user_id'])

    context = {
        'wishlist': wishlist,
		'self': user_object
        }
    return render(request, 'pythonBBApp/dashboard.html', context)

def add(request):
    return render(request, 'pythonBBApp/add.html')

def create(request):
    if request.method == "POST":
        result = WishList.wishListMgr.add(
            item = request.POST['item'],
            user = request.session['user_id']
        )
        if result[0]:
            return redirect(reverse('dashboard'))
        else:
            for error in result[1]:
                messages.add_message(request, messages.INFO, result[1][error])
            return redirect(reverse('add'))
    else:
        return redirect(reverse('add'))

def show_item(request, item_id):
    items = WishList.wishListMgr.get(id=item_id)
    return render(request, 'pythonBBApp/items.html', {'item': items})

def remove(request):
	user_id_object = User.userMgr.get(id=added_by_id)

	return redirect(reverse('dashboard'))

def delete(request, item_id):
    item = WishList.wishListMgr.get(id=item_id)
    item.delete()
    return redirect(reverse('dashboard'))

def logout(request):
    request.session.pop('user_id')
    request.session.pop('user_name')
    return redirect(reverse('index'))
