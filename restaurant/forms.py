from django import forms
from .models import Restaurant, Item
from django.contrib.auth.models import User

class RestaurantForm(forms.ModelForm):
	class Meta:
		model = Restaurant
		exclude = ['owner']

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		exclude = ['restaurant']

class SignupForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name','last_name','username', 'password']

		widgets = {
		'password': forms.PasswordInput(),
		}


class SigninForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())