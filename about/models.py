from django.db import models

# Create your models here.
def about_img(instance,filename):
    imagename , extension = filename.split(".")
    return "postimg/%s.%s"%(instance.about,extension)
class About(models.Model):
    """Model definition for About."""
    what_we_do = models.TextField(max_length=1000)
    our_mission = models.TextField(max_length=1000)
    oru_goals = models.TextField(max_length=1000)
    image=models.ImageField(upload_to='postimg/')
    

    class Meta:
        """Meta definition for About."""

        verbose_name = 'About'
        verbose_name_plural = 'Abouts'

    def __str__(self):
        return str(self.id)
    
    
class FAQ(models.Model):
    """Model definition for FAQ."""
    title=models.CharField(max_length=150)
    description=models.TextField(max_length=3000)

    class Meta:
        """Meta definition for FAQ."""

        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.title