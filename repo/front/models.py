from django.db import models


# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=50)
    s_id = models.CharField(max_length=50, unique=True, blank=False)
    password = models.CharField(max_length=150, blank=False)
    
    def __str__(self):
        return self.name, self.s_id




    