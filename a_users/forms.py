from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image','phone', 'displayname', 'info', 'user_type','gender',]
        widgets = {
            'image': forms.FileInput(),
            'phone' : forms.TextInput(attrs={'placeholder': 'Your phone number'}),
            'displayname' : forms.TextInput(attrs={'placeholder': 'Add display name'}),
            'info' : forms.Textarea(attrs={'rows':3, 'placeholder': 'Add information'}),
            'user_type' : forms.Select(choices=[('tenant','tenant'),('landlord','landlord'),('agent','agent')]),
            'gender' : forms.Select(choices=[('male','male'),('female','female'),('other','other')]),
        }
        
        
class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']
