from django.db import models
from django.db import models

class Tenants(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    adm_no = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Properties(models.Model):
    lot_no = models.IntegerField(unique=True)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE, related_name='properties', null=True, blank=True)
    area = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"Lot {self.lot_no}"


class Payments(models.Model):
    lot_no = models.ForeignKey(Properties, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE, related_name='payments')
    status = models.CharField(max_length=100)  # successful, late, failed
    expected_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def delays(self):
        if self.expected_date and self.payment_date and (self.payment_date > self.expected_date):
            delay = (self.payment_date - self.expected_date).days
            return delay
        return 0

    def __str__(self):
        return f"Payment for Lot {self.lot_no} - {self.tenant.name}"

# Create your models here.
