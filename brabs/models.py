
from django.db import models
from  django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Brab(models.Model):
    auth_user = models.ForeignKey(User, help_text="Brabber")
    title = models.CharField(blank=True, max_length=255, help_text="Brab Title")
    description = models.TextField (help_text="Brab Description")
    visible = models.BooleanField(help_text="Visible")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Brab Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Brab Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def get_absolute_url(self):
        return reverse('brab', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.title

class Category(models.Model):
    auth_user = models.ForeignKey(User, help_text="Creator")
    name = models.CharField(blank=True, max_length=250, help_text="Category Name")
    visible = models.BooleanField(help_text="Visible")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Category Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Category Updated")
    deleted = models.BooleanField(help_text="Deleted")

def get_absolute_url(self):
    return reverse('category', kwargs={"pk": self.id})

def __unicode__(self):
    return self.name

class Category_to_brab(models.Model):
    auth_user = models.ForeignKey(User, help_text="Creator")
    brab = models.ForeignKey(Brab, help_text="Brab")
    category = models.ForeignKey(Category, help_text= "Category")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Updated")
    deleted = models.BooleanField(help_text="Deleted")

def get_absolute_url(self):
    return reverse('category_to_brab', kwargs={"pk": self.id})

def __unicode__(self):
    return self.id

#class Comment(models.Model):
#    created_at = models.DateTimeField(auto_now_add=True)
#    body = models.TextField(verbose_name="Comment")
#    author = models.CharField(verbose_name="Name", max_length=255)
#
#
#class Vote(models.Model):
#    never_mind_count = models.IntegerField( default=0)
#    like_it_count = models.IntegerField( default=0)
#    love_it_count = models.IntegerField( default=0)
#    got_to_have_it_count = models.IntegerField( default=0)
#
#    def create(self):
#        self.like_it_count = 0
#        self.love_it_count = 0
#        self.got_to_have_it_count = 0
#        self.never_mind_count = 0

