from django import forms
from django.forms import ModelForm
from brabs.models import Brab, Comments, Pictures, Category

class BrabForm(ModelForm):

    category = forms.MultipleChoiceField(required=True)
    tags = forms.CharField(max_length=100)
    auth_user = forms.IntegerField(required=False, widget=forms.HiddenInput())
    brab = forms.IntegerField(initial = 0,  required=False, widget=forms.HiddenInput())
    created_at = forms.DateTimeField( required=False, widget=forms.HiddenInput())
    updated_at = forms.DateTimeField( required=False, widget=forms.HiddenInput())
    deleted = forms.BooleanField( required=False, widget=forms.HiddenInput())
    visible = forms.BooleanField( required=False, widget=forms.HiddenInput())


    def __init__(self,*args,**kwargs):
        super (BrabForm,self ).__init__(*args,**kwargs) # populates the brab

        self.fields['category'].choices =\
            [(x.id, x.name) for x in Category.objects.filter(visible=1)]

        # If you really want to do it in views.py, the method is the same.
        #
        # myform.fields['category'].choices =\
        # [(x.id, x.name) for x in Category.objects.filter(visible=1)]

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
        help_text='Max. 42MB!')
    pic_height = forms.IntegerField( required=False, widget=forms.HiddenInput())
    pic_width = forms.IntegerField( required=False, widget=forms.HiddenInput())
    brab = forms.IntegerField( required=False, widget=forms.HiddenInput())
    created_at = forms.DateTimeField( required=False, widget=forms.HiddenInput())
    updated_at = forms.DateTimeField( required=False, widget=forms.HiddenInput())
    deleted = forms.BooleanField( required=False, widget=forms.HiddenInput())
    visible = forms.BooleanField( required=False, widget=forms.HiddenInput())

    class Meta:
        model = Pictures









