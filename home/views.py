from django.shortcuts import render
from cars.models import Car
from accounts.models import WishlistItems

def index(request):
    # Retrieve search parameters from the request
    car_model = request.GET.get('car-model')
    monthly_pay = request.GET.get('monthly-pay')
    year = request.GET.get('year')

    # Initialize queryset with all cars
    cars = Car.objects.all()
    wishlist_item_uids = []
    if request.user.is_authenticated:
        wishlist_items = WishlistItems.objects.filter(wishlist__user=request.user, wishlist__is_paid=False)
        wishlist_item_uids = [item.car.uid for item in wishlist_items]
    # Apply filters based on search parameters, if provided
    if car_model:
        cars = cars.filter(car_brand__icontains=car_model)
    if monthly_pay:
        cars = cars.filter(price__lte=monthly_pay)
    if year:
        cars = cars.filter(year__gte=year)

    # Check if any search parameters were provided
    if car_model or monthly_pay or year:
        context = {'cars': cars,
                   'wishlist_item_uids': wishlist_item_uids,
                   }
    else:
        # If no search parameters were provided, display all cars
        context = {'featured_cars': cars,
                   'wishlist_item_uids': wishlist_item_uids,
                   }

    return render(request, 'home/index.html', context)

def about(request):
    return render(request, 'home/about_us.html')

def contact(request):
    return render(request,'home/contact.html')