from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone
from django_countries.fields import CountryField
from django.utils.text import slugify
User = get_user_model()
# Create your models here.
def image_upload(instance,filename):
    imagename , extension = filename.split(".")
    return "property/%s.%s"%(instance.slug,extension)
def p_image_upload(instance,filename):
    imagename , extension = filename.split(".")
    return "property_image/%s.%s"%(instance.slug,extension)
def place_image_upload(instance,filename):
    imagename , extension = filename.split(".")
    return "place_image/%s.%s"%(instance.slug,extension)

class Property(models.Model):
    user = models.ForeignKey(User, related_name="property_owner", on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    image=models.ImageField( upload_to=image_upload)
    price=models.IntegerField(default=0)
    description=models.TextField(max_length=10000)
    place=models.ForeignKey('Place',related_name='property_place',on_delete=models.CASCADE)
    category=models.ForeignKey('Category',related_name='croperty_category',on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    slug=models.SlugField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Propertys'
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug= slugify(self.name)
        else:
            self.slug= slugify(self.name)
        super(Property, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("property:property_detail", kwargs={'slug' : self.slug})
    
    def check_vailability(self):
        all_reservation = self.book_property.all()
        now = timezone.now().date()
        availability = 'Available' 

        for reservation in all_reservation:
            if now > reservation.date_to:
                availability = 'Available'
            elif now >= reservation.date_from and now <= reservation.date_to:
                reserved_to = reservation.date_to
                availability = f'In progress to {reserved_to}'
            else:
                reserved_to = reservation.date_to
                reserved_from = reservation.date_from
                availability = f'booked from {reserved_from} to {reserved_to} '

        return availability
    
    # def check_vailability(self):
    #     all_reservation=self.book_property.all()
    #     now=timezone.now().date()
        
    #     for reservation in all_reservation :
    #         if now > reservation.date_to:
    #             return 'Avialable'
    #         elif now >= reservation.date_from and now <= reservation.date_to:
    #             return 'In progress'
    #     else:
    #         return 'Avialable'


    def get_avg_rating(self):
        all_reviews=self.review_property.all()
        all_rating=0
        
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_rating += review.rate
            return round(all_rating / len(all_reviews),2)
        else:
            return '-'    
    def len_commnets(self):
        all_commnets = self.review_property.all()
        if all_commnets:
            return len(all_commnets)
        else:
            return '-'
    
class PropertyImages(models.Model):
    property=models.ForeignKey(Property ,related_name='property_image',on_delete=models.CASCADE)
    image=models.ImageField(upload_to=p_image_upload)
    slug=models.SlugField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug= slugify(self.property)
        else:
            self.slug= slugify(self.property)
        super(PropertyImages, self).save(*args, **kwargs)
    class Meta:
        verbose_name = 'PropertyImages'
        verbose_name_plural = 'PropertyImages'
    def __str__(self):
        return str(self.property)


class Place(models.Model):
    name=models.CharField(max_length=50)
    country=CountryField(blank_label='select country')
    image=models.ImageField(upload_to=place_image_upload,blank=True, null=True)
    slug=models.SlugField(blank=True, null=True)
    
    
    
    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug= slugify(self.name)
        else:
            self.slug= slugify(self.name)
        super(Place, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class Category(models.Model):
    name=models.CharField(max_length=50)
    icon=models.CharField(max_length=30)

    class Meta:

        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'

    def __str__(self):
        return self.name

class PropertyReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name='review_property')
    rate=models.IntegerField(default=0)
    feedback=models.TextField(verbose_name=_("comment"))
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')


    class Meta:
        verbose_name = 'PropertyReview'
        verbose_name_plural = 'PropertyReviews'

    def __str__(self):
        return str(self.property)


class PropertyBook(models.Model):
    COUNTGU=(
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    )
    COUNTCH=(
        (None,None),
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name='book_property')
    Created_At= models.DateTimeField(verbose_name=_("Created At"), default=datetime.now)
    date_from=models.DateField(default=timezone.now)
    date_to=models.DateField(default=timezone.now)
    guest=models.CharField(max_length=2,choices=COUNTGU)
    children=models.CharField(max_length=2,choices=COUNTCH)

    class Meta:

        verbose_name = 'PropertyBook'
        verbose_name_plural = 'PropertyBooks'

    def __str__(self):
        return  'User: ' +  self.user.username + ' --> Property: ' + str(self.property)

    def in_progress(self):
        now= timezone.now().date()
        return now > self.date_from and now < self.date_to
    in_progress.boolean = True