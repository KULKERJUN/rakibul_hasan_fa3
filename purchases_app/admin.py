from django.contrib import admin
from purchases_app.models import *
# Register your models here.
admin.site.register([UserProfileModel, SupplierModel, PurchaseModel])