from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from user_registration.models import User
from admin_registration.models import CustomUser

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class BigType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class SmallType(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    big_type = models.ForeignKey(BigType, on_delete=models.PROTECT, related_name='small_types', default=1)

    def __str__(self):
        return f'{self.name} - {self.code} (Belongs to: {self.big_type.name})'


class Donation(models.Model):
    date = models.DateField() #date of creating record
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    admin_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='admin_donations', null=True, blank=True)
    payment_method_id = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL,null=True, blank=True) 
    small_type = models.ForeignKey(SmallType, on_delete=models.PROTECT, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='donation amount')
    remarks = models.TextField(blank=True, null=True, max_length=200)

    def save(self, *args, **kwargs):
        
        #Call the clean() method to validate the data before saving
        self.full_clean()

        super(Donation, self).save(*args, **kwargs)

    def __str__(self):
      return f"Donation by {self.user_id.first_name} on {self.date}"
    
    def get_absolute_url(self):
       return reverse('donation_list')
