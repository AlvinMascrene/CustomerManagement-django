from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Customers)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)