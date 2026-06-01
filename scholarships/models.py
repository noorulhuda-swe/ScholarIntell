from django.db import models

class Scholarship(models.Model):
    scholarship_id        = models.CharField(max_length=50, unique=True)
    name                  = models.CharField(max_length=255)
    description           = models.TextField(blank=True)
    level                 = models.CharField(max_length=100)
    host_institution      = models.CharField(max_length=255, blank=True)
    host_country          = models.CharField(max_length=100, blank=True)
    field_of_study        = models.CharField(max_length=255, blank=True)
    fully_funded          = models.BooleanField(default=False)
    what_it_covers        = models.TextField(blank=True)
    special_requirements  = models.TextField(blank=True)
    application_link      = models.URLField(max_length=500, blank=True)
    open_date             = models.CharField(max_length=150, blank=True)
    deadline              = models.CharField(max_length=150, blank=True)
    source_website        = models.URLField(max_length=500, blank=True)
    language_requirements = models.TextField(blank=True)
    notes                 = models.TextField(blank=True)
    last_verified         = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-fully_funded', 'name']

    def __str__(self):
        return self.name