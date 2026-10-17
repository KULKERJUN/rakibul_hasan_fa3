from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = '__all__'
        exclude = ['user']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = SupplierModel
        fields = '__all__'
        exclude = ['user']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseModel
        fields = '__all__'
        exclude = ['user','subtotal','total_amount','due_amount']

        widgets = {
            'purchase_date': forms.DateInput(
                attrs={'type': 'date'}
            )
        }