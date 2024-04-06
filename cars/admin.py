from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Fuel)
admin.site.register(Gearbox)

class CarImageAdmin(admin.StackedInline):
    model = CarImage

class CarAdmin(admin.ModelAdmin):
    list_display = ['car_name','price']
    inlines = [CarImageAdmin]

admin.site.register(Car,CarAdmin)
admin.site.register(CarImage)
admin.site.register(Coupon)