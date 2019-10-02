from django.db import models

# https://www.techiediaries.com/django-rest-image-file-upload-tutorial/
# Create your models here.
class File(models.Model):
    file = models.FileField(upload_to='file_upload')
    uploaded_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name