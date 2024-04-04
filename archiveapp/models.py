from django.db import models

class MediaFile(models.Model):
    FILE_TYPE_CHOICES = (
        ('video', 'Video'),
        ('image', 'Image'),
        ('document', 'Document'),
        ('audio', 'Audio'),
    )

    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, default='image')
    title = models.CharField(max_length=255)
    description = models.TextField(default='')
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
