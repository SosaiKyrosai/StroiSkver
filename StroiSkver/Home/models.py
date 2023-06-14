from django.db import models

class paper(models.Model):
    title = models.CharField('Название', max_length=100)
    textOfPaper = models.TextField('ТекстСтатьи')
    pictureOfPaper = models.ImageField(blank=True, upload_to='images/')



    def __str__(self):
        return str(self.title)
