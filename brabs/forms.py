from django import forms
from django.forms import ModelForm
from brabs.models import Brab, Comments

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







