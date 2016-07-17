from django.db import models
from django.forms import ModelForm
from django import forms

class Upload(models.Model):
    
    files = models.FileField("File", upload_to="files/")    
    upload_date=models.DateTimeField(auto_now_add =True)

# FileUpload form class.
class UploadForm(ModelForm):
    class Meta:
        model = Upload
        exclude = []

#Min/Max Text Fields
class minmax(forms.Form):
    min = forms.IntegerField()
    max = forms.IntegerField()
    
# Create your models here.
