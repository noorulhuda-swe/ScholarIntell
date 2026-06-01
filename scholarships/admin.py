from django.contrib import admin
from .models import Scholarship

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display  = ('scholarship_id', 'name', 'level', 'host_country', 'fully_funded', 'deadline')
    list_filter   = ('fully_funded', 'level', 'host_country')
    search_fields = ('name', 'description', 'field_of_study', 'host_country')
