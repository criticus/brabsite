from django.http import Http404, HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView, ListView
from brabs.forms import BrabForm, CommentForm, PictureForm, BrabFormSet, VotingForm
from brabs.models import Brab, Pictures, Comments, Tag, Tag_to_brab, Category, Category_to_brab, Vote, Vote_to_brab, Vote_totals
from brabs.models import LoggedInMixin
from django.shortcuts import render_to_response
import re


def hello(request):
    return HttpResponse("Hello world")

class BrabDetailView(DetailView):
    methods = ['get', 'post']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(prefix="C")
        picture_form = PictureForm(prefix="P")
#        Find if this user have voted already
        existing_vote = Vote_to_brab.objects.filter(auth_user_id = request.user.id, brab_id=self.object.pk, )
        if not existing_vote:
            voting_form = VotingForm(prefix="V")
            context = self.get_context_data(object=self.object, C_form=comment_form, P_form=picture_form, V_form=voting_form)
        else:
            context = self.get_context_data(object=self.object, C_form=comment_form, P_form=picture_form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'V' in request.POST:
            comment_form = CommentForm(prefix="C")
            picture_form = PictureForm(prefix="P")
            voting_form = VotingForm(data=request.POST, prefix="V")

            if voting_form.is_valid():
                chosen_vote_id = int(voting_form.cleaned_data['vote_choice'])
                vote_link = Vote_to_brab(auth_user_id = request.user.id, brab_id = self.object.pk, vote_id = chosen_vote_id)
                vote_link.save()

                existing_vote_total = Vote_totals.objects.filter(brab_id=self.object.pk, vote_id=chosen_vote_id)
                if not existing_vote_total:
                    vote_total = Vote_totals(brab_id = self.object.pk, vote_id = chosen_vote_id, total = 1)
                else:
                    vote_total = Vote_totals.objects.get(brab_id=self.object.pk, vote_id=chosen_vote_id)
                    vote_total.total = vote_total.total + 1

                vote_total.save()

                return HttpResponseRedirect(self.object.get_absolute_url())

        if 'C' in request.POST:
            comment_form = CommentForm(data=request.POST, prefix="C")
            picture_form = PictureForm(prefix="P")
            voting_form = VotingForm(prefix="V")
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
            voting_form = VotingForm(prefix="V")
            if picture_form.is_valid():

               if self.object.pictures_set.count():
                   picture_title = picture_form.cleaned_data['title'].title()
                   title_counter = 0
                   while self.object.pictures_set.filter(title__exact=picture_title):
                       title_counter = title_counter + 1
                       picture_title = picture_title + ' '+ str(title_counter).zfill(3)
                       picture_form.instance.title = picture_title

               if not self.object.pictures_set.count():
                    picture_form.instance.main = 1
               elif picture_form.instance.main:

                    for picture in self.object.pictures_set.all():
                        picture.main = 0
                        picture.save()

                #            Fill picture.brab_id with pk of the current brab
               picture_form.instance.brab_id = self.object.pk
               picture_form.instance.visible = 1
               picture_form.save()
               return HttpResponseRedirect(self.object.get_absolute_url())

        context = self.get_context_data(object=self.object, C_form=comment_form, P_form=picture_form, V_form=voting_form)
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

        brabform = BrabForm(data=request.POST)

        if brabform.is_valid():
        #            Fill comments.auth_user_id with request.user.id
            brabform.instance.auth_user_id = request.user.id
            #            Fill comments.brab_id with pk of the current brab
            tags = brabform.cleaned_data['tags']
            tags = self.parse_tags(tags)
            category = brabform.cleaned_data['category']

            brab = brabform.save(commit=False)
            brabformset = BrabFormSet(request.POST, request.FILES, instance=brab)
            if brabformset.is_valid():
                brab.save()
                picture = brabformset.save(commit=False)
                picture[0].visible = 1
                picture[0].main = 1
                picture[0].save()
                tag_count = self.add_tag_records(tags, request.user.id, brab.pk)
                category_count = self.add_category_records(category, request.user.id, brab.pk)
                return HttpResponseRedirect(brab.get_absolute_url())
        else:

            brabformset = BrabFormSet(request.POST, request.FILES)

        self.object = None
        context = self.get_context_data(object=self.object, brabform=brabform, brabformset=brabformset)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.object = Brab()
        brabform = BrabForm(instance=Brab())
        brabformset = BrabFormSet(instance=Brab())
        context = self.get_context_data(object=self.object, brabform=brabform, brabformset=brabformset)
        return self.render_to_response(context)

    def parse_tags(self, tags):
        tags = tags.lower()
        tags = re.split('; |, |,|;', tags)
        return tags

    def add_tag_records(self, tags, user_id, brab_id):
        tag_count = 0
        for tag_text in tags:
            tag_count = tag_count + 1
            existing_tags = Tag.objects.filter(tag__exact=tag_text)
            if not existing_tags:
                tag_object = Tag(auth_user_id = user_id, tag = tag_text, visible = True)
                tag_object.save()
                tag_link = Tag_to_brab(auth_user_id = user_id, brab_id = brab_id, tag_id = tag_object.pk)
            else:
                existing_tag = Tag.objects.get(tag__exact=tag_text)
                tag_link = Tag_to_brab(auth_user_id = user_id, brab_id = brab_id, tag_id = existing_tag.pk)

            tag_link.save()

        return tag_count

    def add_category_records(self, categories, user_id, brab_id):
        category_count = 0
        for categ_id in categories:
            category_count = category_count + 1
            category_link = Category_to_brab(auth_user_id = user_id, brab_id = brab_id, category_id = categ_id)

            category_link.save()

        return category_count

class BrabListView(LoggedInMixin, ListView):
    template_name = 'brabs/brab_list.html'
    paginate_by = 25
    context_object_name = 'posts'

    def get_queryset(self):
        return Brab.objects.filter(auth_user_id=self.request.user.id)