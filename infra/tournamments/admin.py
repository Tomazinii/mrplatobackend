from django.contrib import admin

# Register your models here.

from .models import Group, Members

admin.site.register(Group)
admin.site.register(Members)

