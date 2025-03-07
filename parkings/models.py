from django.db import models
from users.models import User

class Lot(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Parking(models.Model):
    number = models.CharField(max_length=10)
    visit_parking = models.BooleanField(default=False)
    #hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parkings')
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='parkings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('number', 'lot')
        ordering = ['lot', 'number']

    def __str__(self):
        return f"{self.lot.name} - {self.number}"
