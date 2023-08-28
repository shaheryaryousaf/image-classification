from django import forms
from django.forms import ModelForm
from .models import Images


# Image Creation Form
class ImageForm(ModelForm):
    class Meta:
        model = Images
        fields = '__all__'

    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
