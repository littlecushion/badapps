from django.contrib import admin

# Register your models here.
from .models import *

# class AppsAdmin(admin.ModelAdmin):
#     list_displaay=('name','type','size','url')

admin.site.register(Apps)
admin.site.register(Editions)