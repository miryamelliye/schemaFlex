from django.db import models

class Table(models.Model):
    name = models.CharField(max_length=255)

class Field(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=32)
