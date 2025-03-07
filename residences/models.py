""" from django.db import models
from users.models import User

class BlockName(models.Model):
    name = models.CharField(max_length=100)

class Residence(models.Model):
    number = models.CharField(max_length=10)
    block_name = models.ForeignKey(BlockName, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE) """

# residences/models.py (updated)
from django.db import models
from users.models import User

class BlockName(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Residence(models.Model):
    number = models.CharField(max_length=10)
    block_name = models.ForeignKey(BlockName, on_delete=models.CASCADE, related_name='residences')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='residences')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('number', 'block_name')
        ordering = ['block_name', 'number']

    def __str__(self):
        return f"{self.block_name} - {self.number}"