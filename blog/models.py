from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
User = get_user_model()
# Create your models here.
def image_upload(instance,filename):
    imagename , extension = filename.split(".")
    return "postimg/%s.%s"%(instance.slug,extension)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    tag = TaggableManager()
    image=models.ImageField(upload_to=image_upload)
    created_on=models.DateField(default=timezone.now)
    description=models.TextField(max_length=10000)
    category=models.ForeignKey('Category',related_name='postcategory',on_delete=models.CASCADE)
    slug=models.SlugField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            words = self.title.split()[:2]
            self.slug = slugify('-'.join(words))
        else:
            words = self.title.split()[:2]
            self.slug = slugify('-'.join(words))
        super(Post, self).save(*args, **kwargs)
        
    class Meta:

        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("post:post_detail", kwargs={'slug' : self.slug})
    
    def len_commnets(self):
        all_commnets = self.review_post.all()
        if all_commnets:
            return len(all_commnets)
        else:
            return '-'
    
    # def get_len_all_commnets(self):
    #     all_commnets=self.review_post.all()
    #     len_comment=0
        
    #     if len(all_commnets) > 0:
    #         for review in all_commnets:
    #             len_comment += review.message
    #         return len_comment / len(all_commnets)
    #     else:
    #         return '-'    

class Category(models.Model):
    name=models.CharField(max_length=50)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'


    def __str__(self):
        return self.name
    
class AddComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property=models.ForeignKey(Post,related_name='review_post', on_delete=models.CASCADE,verbose_name=_("post"))
    message=models.TextField(max_length=10000)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes_comment')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes_comment')
    

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return  'User: ' +  self.user.username + ' --> post: ' + str(self.property)
