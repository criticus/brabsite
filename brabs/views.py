from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView, ListView
from brabs.forms import BrabForm, CommentForm, PictureForm
from brabs.models import Brab, Pictures, Comments
from brabs.models import LoggedInMixin
from django.forms.models import modelformset_factory, inlineformset_factory

def hello(request):
    return HttpResponse("Hello world")

class BrabDetailView(DetailView):
    methods = ['get', 'post']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(prefix="C")
        picture_form = PictureForm(prefix="P")

        context = self.get_context_data(object=self.object, C_form=comment_form, P_form=picture_form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'C' in request.POST:
            comment_form = CommentForm(data=request.POST, prefix="C")
            picture_form = PictureForm(prefix="P")
            if comment_form.is_valid():
    #            Fill comments.auth_user_id with request.user.id
                comment_form.instance.auth_user_id = request.user.id
    #            Fill comments.brab_id with pk of the current brab
                comment_form.instance.brab_id = self.object.pk
                comment_form.save()
                return HttpResponseRedirect(self.object.get_absolute_url())

        if 'P' in request.POST:
            comment_form = CommentForm(prefix="C")
            picture_form = PictureForm(data=request.POST, prefix="P", files=request.FILES )
            if picture_form.is_valid():
                #            Fill comments.brab_id with pk of the current brab
                comment_form.instance.brab_id = self.object.pk
                picture_form.save()
                return HttpResponseRedirect(self.object.get_absolute_url())

        context = self.get_context_data(object=self.object, C_form=comment_form, P_form=picture_form)
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

class BrabAddView(CreateView):
    methods = ['get', 'post']
    context_object_name="brab"
    template_name = "brabs/brab_add.html"
#    Note absence of parenthesis around the form_class and model names below!
    form_class = BrabForm
    model = Brab

    def post(self, request, *args, **kwargs):

        form = BrabForm(data=request.POST)

        if form.is_valid():
        #            Fill comments.auth_user_id with request.user.id
            form.instance.auth_user_id = request.user.id
            #            Fill comments.brab_id with pk of the current brab

            brab = form.save(commit=False)
            brab.save()
            return HttpResponseRedirect(brab.get_absolute_url())

        self.object = None
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)


class BrabListView(LoggedInMixin, ListView):
    template_name = 'brabs/brab_list.html'
    paginate_by = 25
    context_object_name = 'posts'

    def get_queryset(self):
        return Brab.objects.filter(auth_user_id=self.request.user.id)