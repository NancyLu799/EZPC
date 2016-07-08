from django.db import models
from django.forms import ModelForm

class Upload(models.Model):
    
    files = models.FileField("File", upload_to="files/")    
    upload_date=models.DateTimeField(auto_now_add =True)

# FileUpload form class.
class UploadForm(ModelForm):
    class Meta:
        model = Upload
        exclude = []
# Create your models here.
