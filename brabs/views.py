from django import http
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from brabs.forms import CommentForm

class BrabDetailView(DetailView):
    methods = ['get', 'post']

#    def dispatch(self, request, *args, **kwargs):
#        if not request.user.is_authenticated():
#            return HttpResponse("You can't vote in on this brab.")
#        return super(BrabDetailView, self).dispatch(request, *args, **kwargs)
# see http://www.gregaker.net/2012/apr/19/how-do-django-class-based-views-work/

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(object=self.object)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(object=self.object, data=request.POST)

        if request.POST.__contains__('VoteIt'):
            if request.POST['VoteIt'] == 'VoteItL':
                self.object.like_it_count = self.object.votes.like_it_count + 1
            if request.POST['VoteIt'] == 'VoteItO':
                self.object.love_it_count = self.object.votes.love_it_count + 1
            if request.POST['VoteIt'] == 'VoteItG':
                self.object.got_to_have_it_count = self.object.votes.got_to_have_it_count + 1
            if request.POST['VoteIt'] == 'VoteItN':
                self.object.never_mind_count = self.object.votes.never_mind_count + 1

            form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
            
        if form.is_valid():

            form.save()
            return HttpResponseRedirect(self.object.get_absolute_url())

        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)