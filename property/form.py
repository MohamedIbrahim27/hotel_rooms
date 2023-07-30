from django import forms
from .models import Property,PropertyImages
from django.forms import inlineformset_factory

class PropertyImagesForm(forms.ModelForm):
    class Meta:
        model = PropertyImages
        fields = ['image']
        
# PropertyImagesFormSet = inlineformset_factory(Property, PropertyImages, form=PropertyImagesForm, extra=1)