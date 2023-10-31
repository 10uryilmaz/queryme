from django.contrib import admin
from .models import UploadedData

# Register your models here.
@admin.register(UploadedData)
class UploadedDataAdmin(admin.ModelAdmin):
    list_display = ('data', 'table_name') 
    search_fields = ('data', 'table_name')
    list_filter = ('data', 'table_name') 