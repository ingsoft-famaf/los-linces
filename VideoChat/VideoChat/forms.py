from django import forms

class UploadFileForm(forms.Form):
  video_file = forms.FileField(
      label='Select a video',
      help_text='max. 20 megabytes'
  )
