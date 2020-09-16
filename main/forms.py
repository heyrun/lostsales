from django.forms import ModelForm
from django import forms
from .models import Lostsales, Products
from django.contrib.auth.models import User


class LostsalesForm(ModelForm):
    product = forms.CharField(max_length=200, required=False)
    quantity = forms.IntegerField()

    class Meta:
        model = Lostsales
        fields = ('quantity', 'product')


class UserCreationForm(ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'password')
