from django.contrib import admin

from .models import Item
from .models import Receipt
from .models import Category

admin.site.register(Item)
admin.site.register(Receipt)
admin.site.register(Category)
