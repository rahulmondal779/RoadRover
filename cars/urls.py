from django.urls import path
from cars.views import get_cars,feature_cars,add_to_wishlist,remove_from_wishlist,wishlist_page

urlpatterns = [
    path('featured-cars/',feature_cars,name="featured_cars"),
    path('<slug>/',get_cars,name="car_info"),
    path('wishlist/items/',wishlist_page,name='wishlist'),
    path('wishlist/<uid>/', add_to_wishlist ,name='add_to_wishlist'),
    path('remove_from_wishlist/<uid>/', remove_from_wishlist, name='remove_from_wishlist'),
]