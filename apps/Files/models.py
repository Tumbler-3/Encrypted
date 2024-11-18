from django.db import models

class FileModel(models.Model):
    file = models.FileField(null=False, blank=False)
    key = models.FileField(null=True, blank=True)
    
    def delete(self, *args, **kwargs):
        self.file.delete()
        self.key.delete()
        super(FileModel, self).delete(*args, **kwargs)