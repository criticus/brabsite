from django import forms
from django.forms import ModelForm
from brabs.models import Comments
from django.contrib.auth.models import User

class CommentForm(ModelForm):

    auth_user = forms.IntegerField( required=False, widget=forms.HiddenInput())
    brab = forms.IntegerField( required=False, widget=forms.HiddenInput())

    class Meta:
        model = Comments


#
#    def __init__(self, *args, **kwargs):
##        if user_id:
##            if not kwargs.get('data',{}):
###                ModelForm is created first time to display
###                initially blank fields
##               initial_value = kwargs.get('auth_user', {})
##               initial_value['auth_user'] = user_id
##               kwargs['initial'] = initial_value
##
###            else:
###               ModelForm is created with data from the request.POST
###               the following won't work - inmmutable QueryDict
###               kwargs.get('data',{}).update({'auth_user':user_id})
##
#        super(CommentForm, self).__init__(*args, **kwargs)






