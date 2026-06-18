from django.contrib import admin
from .models import Items, Restuarant, User, Cart

# Register your models here.
admin.site.register(User)
admin.site.register(Restuarant)
admin.site.register(Items)
admin.site.register(Cart)