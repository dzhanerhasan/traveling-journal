from django.contrib import admin

# Register your models here.
from finalProject.checklist.models import CheckList, ListItems

admin.site.register(CheckList)
admin.site.register(ListItems)