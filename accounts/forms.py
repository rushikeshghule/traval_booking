from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignupForm(UserCreationForm):
    """Form for user registration"""
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        
        return user

class ProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_pic')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
