from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileModel(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE, related_name = 'user_profile', null=True)
    full_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=11, null=True)
    address = models.CharField(max_length=110,null=True)
    picture = models.ImageField(upload_to = 'media/profile_image', null=True)

    def __str__(self):
        return f'{self.full_name}'

class SupplierModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supplier_profile', null = True)
    supplier_name = models.CharField(max_length=100,null=True)
    contact_number = models.CharField(max_length=11,null=True)
    address = models.TextField(null=True)

    def __str__(self):
        return f'{self.supplier_name}'

class PurchaseModel(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'purchase_profile', null=True)
    supplier = models.ForeignKey(SupplierModel,on_delete = models.SET_NULL, related_name = 'purchase_supplier', null = True)
    product_name = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)
    unit_price = models.FloatField(null = True)
    discount = models.FloatField(null=True)
    paid_amount = models.FloatField(null=True)
    purchase_date = models.DateField(null = True)
    subtotal = models.FloatField(null = True)
    total_amount = models.FloatField(null=True)
    due_amount = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return f'{self.product_name}-{self.user.username}'

    