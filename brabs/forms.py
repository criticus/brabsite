from django import forms
from django.forms import ModelForm
from brabs.models import Brab, Comments, Pictures

class BrabForm(ModelForm):

    auth_user = forms.IntegerField(required=False, widget=forms.HiddenInput())
    brab = forms.IntegerField(initial = 0,  required=False, widget=forms.HiddenInput())
    created_at = forms.DateTimeField( required=False, widget=forms.HiddenInput())
    updated_at = forms.DateTimeField( required=False, widget=forms.HiddenInput())
    deleted = forms.BooleanField( required=False, widget=forms.HiddenInput())
    visible = forms.BooleanField( required=False, widget=forms.HiddenInput())

    class Meta:
        model = Brab

class CommentForm(ModelForm):

    auth_user = forms.IntegerField( required=False, widget=forms.HiddenInput())
    brab = forms.IntegerField( required=False, widget=forms.HiddenInput())
    created_at = forms.DateTimeField( required=False, widget=forms.HiddenInput())
    updated_at = forms.DateTimeField( required=False, widget=forms.HiddenInput())
    deleted = forms.BooleanField( required=False, widget=forms.HiddenInput())
    visible = forms.BooleanField( required=False, widget=forms.HiddenInput())

    class Meta:
        model = Comments

class PictureForm(ModelForm):

    title = forms.CharField(label='Title')
    picture = forms.ImageField(label='Select a file',
        help_text='max. 42 megabytes')
    pic_height = forms.IntegerField( required=False, widget=forms.HiddenInput())
    pic_width = forms.IntegerField( required=False, widget=forms.HiddenInput())
    brab = forms.IntegerField( required=False, widget=forms.HiddenInput())
    created_at = forms.DateTimeField( required=False, widget=forms.HiddenInput())
    updated_at = forms.DateTimeField( required=False, widget=forms.HiddenInput())
    deleted = forms.BooleanField( required=False, widget=forms.HiddenInput())
    visible = forms.BooleanField( required=False, widget=forms.HiddenInput())

    class Meta:
        model = Pictures









