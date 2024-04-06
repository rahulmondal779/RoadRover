from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from cars.models import Car,Coupon



class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
    
    def get_wishlist_count(self):
        if hasattr(self, 'user') and hasattr(self.user, 'carts'):
            return WishlistItems.objects.filter(wishlist__user=self.user, wishlist__is_paid=False).count()
        return 0
    
class ProfileImage(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_images")
    image = models.ImageField(upload_to='profile')

    
class Cart(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_total_price(self):
        price = self.car.price
        return price    
    

class WishlistItems(BaseModel):
    wishlist = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='wishlist_items')
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
        
    def get_car_price(self):
        price = [self.car.price]
        return price


@receiver(post_save , sender = User)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user = instance , email_token = email_token)
            email = instance.email
            send_account_activation_email(email , email_token)

    except Exception as e:
        print(e)