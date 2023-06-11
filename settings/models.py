from django.db import models

# Create your models here.

def settings_img(instance,filename):
    imagename , extension = filename.split(".")
    return "postimg/%s.%s"%(instance.site_name,extension)

class Settings(models.Model):
    """Model definition for Settings."""
    site_name=models.CharField(max_length=50)
    logo=models.ImageField(upload_to=settings_img)
    phone=models.CharField(max_length=20)
    email=models.EmailField(max_length=254)
    description=models.TextField(max_length=500)
    fb_link=models.URLField(max_length=200)
    inst_link=models.URLField(max_length=200)
    twitter_link=models.URLField(max_length=200)
    adress=models.CharField(max_length=100)
    class Meta:

        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return self.site_name
