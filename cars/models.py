from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

# Fuel Type
class Fuel(BaseModel):
    fuel_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null= True, blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.fuel_name)
        super(Fuel, self).save(*args, **kwargs)
    def __str__(self) -> str:
        return self.fuel_name


# Automatic, Manual or Hybrid
class Gearbox(BaseModel):
    gearbox_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null =True, blank=True)
    def save(self,*args,**kwargs):
        self.slug = slugify(self.gearbox_name)
        super(Gearbox, self).save(*args,**kwargs)
    def __str__(self) -> str:
        return self.gearbox_name

# car
class Car(BaseModel):
    car_brand = models.CharField(max_length=100)
    car_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True,blank=True)
    car_description = models.CharField(max_length=1000)
    fuel_type = models.ForeignKey(Fuel,on_delete=models.CASCADE, related_name="Cars")
    price = models.IntegerField()
    seat = models.IntegerField()
    gearbox = models.ForeignKey(Gearbox,on_delete=models.CASCADE,related_name="Gearbox")
    mileage =  models.IntegerField()
    year = models.IntegerField()
    car_image = models.ImageField(upload_to="car")

    def save(self, *args,  **kwargs):
        self.slug = slugify(self.car_name)
        super(Car,self).save(*args,**kwargs)
    
    def __str__(self) -> str:
        return self.car_name
    
class CarImage(BaseModel):
    car = models.ForeignKey(Car,on_delete=models.CASCADE,related_name="Car_Image")
    image = models.ImageField(upload_to="car")

class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default = 100)
    minimum_amount = models.IntegerField(default=500)
    def __str__(self) -> str:
        return self.coupon_code