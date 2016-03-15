from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 128, unique = True)
    catviews = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.name = self.name.replace(' ','-').lower()
        if self.catviews < 0:
            self.catviews = 0
        super(Category,self).save(*args,**kwargs)

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length = 128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    first_visit = models.DateTimeField(default=datetime.now)
    last_visit = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.first_visit > datetime.now():
            self.first_visit = datetime.now()
        if self.last_visit > datetime.now():
            self.last_visit = datetime.now()
        if self.first_visit > self.last_visit:
            self.last_visit = datetime.now()
        super(Page,self).save(*args,**kwargs)

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username