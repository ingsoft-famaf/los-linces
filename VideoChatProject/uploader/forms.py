from django import forms
from .validators import validate_file_extension

class UploadFileForm(forms.Form):
  title = forms.CharField(label="Title", max_length=50)
  description = forms.CharField(label="Description", widget=forms.Textarea)
  video_file = forms.FileField(
      label='Select a video',
      help_text='max. 20 megabytes',
      validators=[validate_file_extension]
  )
