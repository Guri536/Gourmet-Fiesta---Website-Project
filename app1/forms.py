from django import forms
from .models import img

class image_fl(forms.ModelForm):
        class Meta:
            model = img
            fields = ['name', 'imag']