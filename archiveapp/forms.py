from django import forms
from .models import MediaFile

class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = [ 'title', 'description', 'file_type','file']
