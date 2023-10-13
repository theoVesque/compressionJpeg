from django import forms
from compressionJpeg.listings.models import Image


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('original_image',)
