from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from cars.models import *
from accounts.models import Cart, WishlistItems
from django.contrib.auth.decorators import login_required

def get_cars(request, slug):
    try:
        car = get_object_or_404(Car, slug=slug)
        wishlist_items = WishlistItems.objects.filter(wishlist__user=request.user, wishlist__is_paid=False)
        wishlist_item_uids = [item.car.uid for item in wishlist_items]
    except Exception as e:
        print(e)
        # Handle case where wishlist items couldn't be retrieved
        wishlist_item_uids = []
    
    context = {'car': car, 'wishlist_item_uids': wishlist_item_uids}
    return render(request, 'cars/cars.html', context)


def feature_cars(request):
    try:
        # Retrieve all cars
        all_cars = Car.objects.all()
        wishlist_item_uids = []
        # Retrieve wishlist items for the current user
        user = request.user
        if request.user.is_authenticated:
            wishlist_items = WishlistItems.objects.filter(wishlist__user=user, wishlist__is_paid=False)
            wishlist_item_uids = [item.car.uid for item in wishlist_items]

        # Pass the cars and wishlist_item_uids to the template context
        context = {'cars': all_cars, 'wishlist_item_uids': wishlist_item_uids}
        
        return render(request, 'cars/feature.html', context)
    except Exception as e:
        print(e)

@login_required
def add_to_wishlist(request, uid):
    car  =  get_object_or_404(Car,uid = uid)
    user = request.user
    wishlist, _ = Cart.objects.get_or_create(user = user, is_paid = False)
    wishlist_items = WishlistItems.objects.create(wishlist = wishlist, car = car)
    
    wishlist_items.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def remove_from_wishlist(request, uid):
    car = get_object_or_404(Car, uid=uid)
    user = request.user
    
    # Retrieve wishlist items for the current user and specific car
    wishlist_items = WishlistItems.objects.filter(wishlist__user=user, wishlist__is_paid=False, car=car)
    
    # Delete all matching wishlist items
    wishlist_items.delete()
    
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def wishlist_page(request):
    if request.user.is_authenticated:
        wishlist_items = WishlistItems.objects.filter(wishlist__user=request.user, wishlist__is_paid=False)
        context = {'wishlist_items': wishlist_items}
        return render(request, 'cars/wishlist.html', context)
    else:
        # Redirect unauthenticated users to the login page
        return redirect('login')
