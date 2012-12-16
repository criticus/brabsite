from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone

from django import http


class LoggedInMixin(object):
    """ A mixin requiring a user to be logged in. """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise http.Http404
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)

class Brab(models.Model):
    auth_user = models.ForeignKey(User, null=True, blank=True, verbose_name='Brabber', help_text="Brabber")
    title = models.CharField(blank=True, max_length=255, help_text="Brab Title")
    description = models.TextField (help_text="Brab Description")
    visible = models.BooleanField(help_text="Visible")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Brab Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Brab Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
                self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Brab, self).save()

    def get_absolute_url(self):
        return reverse('brab', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.title


class Category(models.Model):
    auth_user = models.ForeignKey(User, null=True, blank=True, help_text="Creator")
    name = models.CharField(blank=True, max_length=250, help_text="Category Name")
    visible = models.BooleanField(help_text="Visible")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Category Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Category Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Category, self).save()

    def get_absolute_url(self):
        return reverse('category', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.name

class Category_to_brab(models.Model):
    auth_user = models.ForeignKey(User, null=True, blank=True, help_text="Creator")
    brab = models.ForeignKey(Brab, help_text="Brab")
    category = models.ForeignKey(Category, help_text= "Category")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Category_to_brab, self).save()

    def get_absolute_url(self):
        return reverse('category_to_brab', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.id

class Comments(models.Model):
    auth_user= models.ForeignKey(User, blank=True, null=True, help_text="Author")
    brab = models.ForeignKey(Brab, blank=True, null=True, help_text="Brab")

    comment = models.TextField (help_text= 'Comment text')

    visible = models.BooleanField(help_text="Visible")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Comment Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Comment Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
            self.created_at = timezone.now()


        self.updated_at = timezone.now()
        super(Comments, self).save()


    def get_absolute_url(self):
        return reverse('comments', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.comment

class Messages(models.Model):
    auth_user_from = models.ForeignKey(User, null=True, blank=True, related_name='auth_user_from', help_text="From")
    auth_user_to = models.ForeignKey(User, null=True, blank=True, related_name='auth_user_to', help_text="To")

    message = models.TextField (help_text= 'Message text')

    visible = models.BooleanField(help_text="Visible")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Message Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Message Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Messages, self).save()

    def get_absolute_url(self):
        return reverse('messages', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.message

class Pictures(models.Model):
    brab = models.ForeignKey(Brab, blank=True, null=True, help_text="Brab")
    title = models.TextField(null=True, help_text="title")
    picture = models.ImageField(upload_to= 'pictures/%Y/%m/%d', height_field="pic_height", width_field="pic_width", null=True, blank=True, max_length=250, help_text="Picture URL")
    pic_height = models.IntegerField(null=True, blank=True)
    pic_width = models.IntegerField(null=True, blank=True)

    main = models.BooleanField(help_text= 'Main')

    visible = models.BooleanField(help_text="Visible")
    created_at = models.DateTimeField(auto_now_add=True, help_text="URL Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="URL Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Pictures, self).save()

    def get_absolute_url(self):
        return reverse('pictures', kwargs = {"pk": self.id})

    def __unicode__(self):
        return self.url


class Tag(models.Model):
    auth_user= models.ForeignKey(User, blank=True, null=True, help_text="Author")
    tag = models.CharField(blank=True, max_length=250, help_text="Tag Name")
    visible = models.BooleanField(help_text="Visible")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Tag, self).save()

    def get_absolute_url(self):
        return reverse('tag', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.tag

class Tag_to_brab(models.Model):
    auth_user= models.ForeignKey(User, null=True, blank=True, help_text="Creator")
    brab = models.ForeignKey(Brab, help_text="Brab")
    tag = models.ForeignKey(Tag, help_text= "Category")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Tag_to_brab, self).save()

    def get_absolute_url(self):
        return reverse('tag_to_brab', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.id

class Vote(models.Model):
    auth_user = models.ForeignKey(User, help_text="Creator")
    name = models.CharField(blank=True, max_length=250, help_text="Vote Name")
    visible = models.BooleanField(help_text="Visible")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Vote, self).save()

    def get_absolute_url(self):
        return reverse('vote', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.tag

class Vote_to_brab(models.Model):
    auth_user = models.ForeignKey(User, null=True, blank=True, help_text="Creator")
    brab = models.ForeignKey(Brab, help_text="Brab")
    vote = models.ForeignKey(Vote, help_text= "Vote")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Tag_to_brab, self).save()

    def get_absolute_url(self):
        return reverse('vote_to_brab', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.id

class Vote_totals(models.Model):
    brab = models.ForeignKey(Brab, help_text="Brab")
    vote = models.ForeignKey(Vote, help_text= "Vote")
    total = models.IntegerField(help_text= "Total")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Vote_totals, self).save()

    def get_absolute_url(self):
        return reverse('vote_totals', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.id

class Attribute(models.Model):
    auth_user = models.ForeignKey(User, help_text="Creator")
    category = models.ForeignKey(Category, help_text="Category")
    name = models.CharField(blank=True, max_length=250, help_text="Category Name")
    visible = models.BooleanField(help_text="Visible")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Category Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Category Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Attribute, self).save()

    def get_absolute_url(self):
        return reverse('attribute', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.name

class Attribute_to_brab(models.Model):
    auth_user = models.ForeignKey(User, null=True, blank=True, help_text="Creator")
    brab = models.ForeignKey(Brab, help_text="Brab")
    attribute = models.ForeignKey(Attribute, help_text= "Category")

    created_at = models.DateTimeField(auto_now_add=True, help_text="Created")
    updated_at = models.DateTimeField(auto_now_add=True, help_text="Updated")
    deleted = models.BooleanField(help_text="Deleted")

    def save(self):
        if self.created_at == None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super(Attribute_to_brab, self).save()

    def get_absolute_url(self):
        return reverse('attribute_to_brab', kwargs={"pk": self.id})

    def __unicode__(self):
        return self.id


