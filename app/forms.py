from django import forms
from .models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _

from django.contrib.auth import password_validation

class CustomerRegistrationForm(UserCreationForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	email = forms.CharField(label='Email', required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}
	
	
	
	
class CustomerProfileForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['name', 'locality', 'city', 'zipcode', 'state']
		widgets = {
			'name':forms.TextInput(attrs={'class':'form-control'}), 'locality':forms.TextInput(attrs={'class':'form-control'}), 'city':forms.TextInput(attrs={'class':'form-control'}), 'state':forms.Select(attrs={'class':'form-control'}),'zipcode':forms.NumberInput(attrs={'class':'form-control'})
		}
		
class LoginForm(AuthenticationForm):
	username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control'}))
	password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autofocus':True, 'class':'form-control'}))
	
	
class MyPasswordChangeForm(PasswordChangeForm):
	pass
	
class MyPasswordResetForm(PasswordResetForm):
	email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))
	
	
class MySetPasswordForm(SetPasswordForm):
	new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}),
	help_text = password_validation.password_validators_help_text_html())
	new_password2 = forms.CharField(label=_("confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autofocus': True, 'class':'form-control'}))
	
	
