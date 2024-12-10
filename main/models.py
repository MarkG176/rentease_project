from datetime import timedelta, date

from django.db import models
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import IntegerField


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
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0000.00)
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
# Signal to create/update payment when a lot is reassigned
@receiver(post_save, sender=Properties)
def create_or_update_payment(sender, instance, **kwargs):
    if instance.tenant:  # Check if a tenant is assigned
        expected_payment_date = date.today() + timedelta(days=30)  # Default expected payment is 30 days from today
        payment, created = Payments.objects.get_or_create(
            lot_no=instance,
            tenant=instance.tenant,
            defaults={'expected_date': expected_payment_date, 'status': 'pending'}
        )
        if not created:
            # If payment exists, update expected date and status
            payment.expected_date = expected_payment_date
            payment.status = 'pending'
            payment.save()

class Incidents(models.Model):
    tenant_name = models.CharField(max_length=255)
    lot_no = models.CharField(max_length=100)
    description = models.TextField()
    is_utility = models.BooleanField(default=False)
    is_social = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incident by {self.tenant_name} in Lot {self.lot_no}"