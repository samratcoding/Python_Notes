from django.contrib import admin
from .models import *                # or from .models import "ModuleName" 


# Add the field to make read-only
class ApiListAdmin(admin.ModelAdmin):
    readonly_fields = ('filled_quota',)  
admin.site.register(ApiList, ApiListAdmin)


# Register your models here.
admin.site.register(Module_Name) 

# Changing the Django Admin Header Text
admin.site.site_header = 'Project Name'    
