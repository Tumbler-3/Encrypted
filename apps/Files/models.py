from django.db import models

class FileModel(models.Model):
    file = models.FileField(null=False, blank=False)