from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    DEGREE_CHOICES = [
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
        ('PhD', 'PhD'),
    ]
    LANGUAGE_CERT_CHOICES = [
        ('', 'None'),
        ('IELTS', 'IELTS'),
        ('TOEFL', 'TOEFL'),
        ('Duolingo', 'Duolingo English Test'),
        ('PTE', 'PTE Academic'),
    ]

    user              = models.OneToOneField(User, on_delete=models.CASCADE, related_name='studentprofile')
    cgpa              = models.FloatField(help_text='Your CGPA out of 4.0')
    degree_level      = models.CharField(max_length=50, choices=DEGREE_CHOICES)
    field_of_study    = models.CharField(max_length=150)
    country_of_origin = models.CharField(max_length=100)
    language_cert     = models.CharField(max_length=50, choices=LANGUAGE_CERT_CHOICES, blank=True, default='')
    language_score    = models.FloatField(null=True, blank=True)
    preferred_country = models.CharField(max_length=100, blank=True)
    profile_complete  = models.BooleanField(default=False)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} — {self.degree_level}"