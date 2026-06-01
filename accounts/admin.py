from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree_level', 'field_of_study', 'cgpa', 'country_of_origin')
    search_fields = ('user__username', 'field_of_study')
