from django.contrib import admin

# Register your models here.
from .models import category, mouseAction, category_MouseAction_Mapping

admin.site.register(category_MouseAction_Mapping)
admin.site.register(category)
admin.site.register(mouseAction)
