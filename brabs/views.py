from django import http
from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from brabs.forms import CommentForm
import datetime
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response

def hello(request):
    return HttpResponse("Hello world")

class BrabDetailView(DetailView):
    methods = ['get', 'post']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm()
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(data=request.POST)

        if form.is_valid():
#            Fill comments.auth_user_id with request.user.id
            form.instance.auth_user_id = request.user.id
#            Fill comments.brab_id with pk of the current brab
            form.instance.brab_id = self.object.pk
            form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())

        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self):
        # Call the superclass
        object = super(BrabDetailView, self).get_object()
        # If necessary, modify the Brab object properties
        # then save it with object.save()
        # Return the object
        return object

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BrabDetailView, self).get_context_data(**kwargs)
        # Add in some context dictionary value
        # context['book_list'] = Book.objects.all()
        return context