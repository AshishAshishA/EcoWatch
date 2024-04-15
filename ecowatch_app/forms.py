from django import forms
from .models import Video, WasteSite

class UploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']

class TagForm(forms.ModelForm):
    class Meta:
        model = WasteSite
        fields = ['name', 'latitude', 'longitude']
