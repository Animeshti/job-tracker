from django.db import models
from django.contrib.auth.models import User 
# Create your models here. 

class JobApplication(models.Model): 
    STATUS_CHOICES = [ 
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offered', 'Offered'), 
        ('Rejected', 'Rejected'), 
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    company_name = models.CharField(max_length=255) 
    job_title = models.CharField(max_length=255) 
    applied_date = models.DateField() 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    notes = models.TextField(blank=True) 

    def __str__(self): 
        return f"{self.company_name} - {self.job_title}" 
    