from django.urls import path
from home.views import index,about,contact

urlpatterns = [
    path('', index,name="index"),
    path('about',about,name="about_us"),
    path('contact',contact,name="contact_us"),
]