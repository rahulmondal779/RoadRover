from django.urls import path
from accounts.views import *




urlpatterns = [
    path('login/',user_login,name="login"),
    path('register/',register,name="register"),
    path('activate/<email_token>/',activate_email, name="activate_email"),
    path('logout/',logging_out,name='logout'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<token>/', reset_password, name='reset_password'),
    path('payment/<slug:car_slug>/',payment_page, name='payment_page'),
    path('success/', success, name='success'),
    path('remove_coupon/', remove_coupon, name='remove_coupon'),
    path('test/',test, name="test"),
]