from django.http import Http404, HttpResponse, HttpRequest
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView, ListView
from brabs.forms import BrabForm, CommentForm, PictureForm, BrabFormSet, VotingForm
from brabs.models import Brab, Pictures, Comments, Tag, Tag_to_brab, Category, Category_to_brab, \
    Vote, Vote_to_brab, Vote_totals, Follower_to_followee
from brabs.models import LoggedInMixin
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.db import models
import re, string



def hello(request):
    return HttpResponse("Hello world (from brabout)!")

class BrabDetailView(DetailView):
    methods = ['get', 'post']

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(prefix="C")
        picture_form = PictureForm(prefix="P")

#        Find if this user have voted already
        existing_vote = Vote_to_brab.objects.filter(auth_user_id = request.user.id, brab_id=self.object.pk, )
        if existing_vote:
            voting_form = VotingForm(prefix="V", initial={'vote_choice':existing_vote._result_cache[0].vote_id})
            current_vote = existing_vote._result_cache[0].vote_id
        else:
            voting_form = VotingForm(prefix="V")
            current_vote = 0
#        Create a data structure (list of dictionaries) with information on available vote choices
#        which one is currently selected by the user, totals of vote for each choice to pass to template in context
        votes_data = []
        current_vote_totals=Vote_totals.objects.filter(brab_id=self.object.pk)
        for x in Vote.objects.filter(visible=1):
            if x.id == current_vote:
                vote_selected = 1
            else:
                vote_selected = 0
            try:
#                vote_total=Vote_totals.objects.get(brab_id=self.object.pk,vote_id=x.id).total
                vote_total=current_vote_totals.get(vote_id=x.id).total
            except:
                vote_total=0
            vote_data = {'id':x.id, 'name':x.name, 'selected':vote_selected, 'total':vote_total}
            votes_data.append(vote_data)

            fq=Follower_to_followee.objects.filter(follower_id=request.user.id, followee_id=self.object.auth_user_id, deleted = 0)
            if fq:
                followed_by_logged_in_user=1
            else:
                followed_by_logged_in_user=0
        context = self.get_context_data(object=self.object, C_form=comment_form, P_form=picture_form, V_form=voting_form,\
            current_vote =  current_vote, votes_data = votes_data, followed_by_logged_in_user=followed_by_logged_in_user)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'SF' in request.POST:
            Follower_to_followee.objects.filter(follower_id = request.user.id, \
                followee_id = self.object.auth_user_id).update(deleted = 1)
            return HttpResponseRedirect(self.object.get_absolute_url())
        if 'F' in request.POST:
            try:
                follower_to_followee = Follower_to_followee.objects.get(follower_id = request.user.id, \
                                                    followee_id = self.object.auth_user_id)
                follower_to_followee.deleted = 0

            except:
                follower_to_followee = Follower_to_followee(follower_id = request.user.id,\
                    followee_id = self.object.auth_user_id )


            follower_to_followee.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        if 'V' in request.POST:
            comment_form = CommentForm(prefix="C")
            picture_form = PictureForm(prefix="P")
            voting_form = VotingForm(data=request.POST, prefix="V")

            if voting_form.is_valid():
                chosen_vote_id = int(voting_form.cleaned_data['vote_choice'])
                existing_vote = Vote_to_brab.objects.filter(auth_user_id = request.user.id, brab_id=self.object.pk, )
                if not existing_vote:
                    vote_link = Vote_to_brab(auth_user_id = request.user.id, brab_id = self.object.pk, vote_id = chosen_vote_id)
                    vote_link.save()
                    existing_vote_total = Vote_totals.objects.filter(brab_id=self.object.pk, vote_id=chosen_vote_id)
                    if not existing_vote_total:
                        vote_total = Vote_totals(brab_id = self.object.pk, vote_id = chosen_vote_id, total = 1)
                    else:
                        vote_total = Vote_totals.objects.get(brab_id=self.object.pk, vote_id=chosen_vote_id)
                        vote_total.total = vote_total.total + 1

                    vote_total.save()
                else:
                    existing_vote = Vote_to_brab.objects.get(auth_user_id = request.user.id, brab_id=self.object.pk, )
                    old_vote_id = existing_vote.vote_id
                    existing_vote.vote_id = chosen_vote_id
                    existing_vote.save()

                    existing_old_vote_total = Vote_totals.objects.filter(brab_id=self.object.pk, vote_id=old_vote_id, )
                    existing_new_vote_total = Vote_totals.objects.filter(brab_id=self.object.pk, vote_id=chosen_vote_id, )
                    if existing_old_vote_total:
                        vote_total = Vote_totals.objects.get(brab_id=self.object.pk, vote_id=old_vote_id)
                        vote_total.total = vote_total.total - 1
                        vote_total.save()

                    if existing_new_vote_total:
                        vote_total = Vote_totals.objects.get(brab_id=self.object.pk, vote_id=chosen_vote_id)
                        vote_total.total = vote_total.total + 1
                    else:
                        vote_total = Vote_totals(brab_id = self.object.pk, vote_id = chosen_vote_id, total = 1)

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
                #            add vote totals - one per each vote choice...
                for x in Vote.objects.filter(visible=1):
                    vote_total = Vote_totals(brab_id = brab.pk, vote_id = x.id, total = 0)
                    vote_total.save()
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

class BrabEditView(CreateView):
    methods = ['get', 'post']
    context_object_name="brab"
    template_name = "brabs/brab_edit.html"
    #    Note absence of parenthesis around the form_class and model names below!
    form_class = BrabForm
    model = Brab

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.auth_user_id  == request.user.id:
            return HttpResponse('<div align="center"><h1>You are not the author of this brab</h1><br>...therefore you may not edit it!</div>')
#        Find what categories and tags is currently edited brab marked with so that
#        appropriate fields would appear pre-filled in the template
        selected_categories = Category_to_brab.objects.filter(brab_id = self.object.pk)
        categories = []
        if selected_categories:
            for category_instance in selected_categories:
                categories.append(category_instance.category_id)

        selected_tags = Tag_to_brab.objects.filter(brab_id = self.object.pk)
        tags = ''
        tag_count = 0
        if selected_tags:
            for tag_instance in selected_tags:
                if tag_count:
                    tags = tags + ', '
                tags = tags + tag_instance.tag.tag
                tag_count = tag_count + 1

        brabform = BrabForm(instance=self.object, initial={'category':categories, 'tags':tags}, prefix="B")
        picture_form = PictureForm(prefix="P")

#        The section below did not work out (actually it did exactly what intended, but
#        then there were a bunch of difficulties in displaying pre-filled formset in template, etc.)

#        brabformset = BrabFormSet(instance=self.object)
##        Fill inline brabformset picture forms with data about attached pictures
#        picture_set = self.object.pictures_set.all()
##        The statement above fires the query
#        test_stru = zip(brabformset.forms, picture_set)
#        for subform, data in test_stru:
#            subform.initial = data

        context = self.get_context_data(object=self.object, brabform=brabform, P_form=picture_form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.auth_user_id  == request.user.id:
            return HttpResponse('<div align="center"><h1>You are not the author of this brab</h1><br>...therefore you may not edit it!</div>')

        brabform = BrabForm(data=request.POST, instance=self.object, prefix="B")

        if brabform.is_valid():

            brabform.instance.auth_user_id = request.user.id

            tags = brabform.cleaned_data['tags']
            tags = self.parse_tags(tags)
            category = brabform.cleaned_data['category']

            brab = brabform.save(commit=False)

            brab.save()
            tag_count = self.add_tag_records(tags, request.user.id, brab.pk)
            category_count = self.add_category_records(category, request.user.id, brab.pk)
            for key in request.POST:
                if key.startswith('delete_') and request.POST[key] == 'on':
                    picture_record_id = re.sub(r"\D", "", key)
                    Pictures.objects.filter(id = picture_record_id).update(deleted = 1)
                if key.startswith('makemain_') and request.POST[key] == 'on':

                    if self.object.pictures_set.count():
                        for picture in self.object.pictures_set.all():
                            picture.main = 0
                            picture.save()

                    picture_record_id = re.sub(r"\D", "", key)
                    Pictures.objects.filter(id = picture_record_id).update(main = 1)
                if key.startswith('hide_') and request.POST[key] == 'on':
                    picture_record_id = re.sub(r"\D", "", key)
                    Pictures.objects.filter(id = picture_record_id).update(visible = 0)
                if key.startswith('show_') and request.POST[key] == 'on':
                    picture_record_id = re.sub(r"\D", "", key)
                    Pictures.objects.filter(id = picture_record_id).update(visible = 1)

            picture_form = PictureForm(data=request.POST, prefix="P", files=request.FILES )
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
            return HttpResponseRedirect(brab.get_absolute_url())
        else:

            #        Find what categories and tags is currently edited brab marked with so that
            #        appropriate fields would appear pre-filled in the template
            selected_categories = Category_to_brab.objects.filter(brab_id = self.object.pk)
            categories = []
            if selected_categories:
                for category_instance in selected_categories:
                    categories.append(category_instance.category_id)

            selected_tags = Tag_to_brab.objects.filter(brab_id = self.object.pk)
            tags = ''
            tag_count = 0
            if selected_tags:
                for tag_instance in selected_tags:
                    if tag_count:
                        tags = tags + ', '
                    tags = tags + tag_instance.tag.tag
                    tag_count = tag_count + 1

            brabform = BrabForm(instance=self.object, initial={'category':categories, 'tags':tags}, prefix="B")
            picture_form = PictureForm(prefix="P")

            # self.object = None
            context = self.get_context_data(object=self.object, brabform=brabform, P_form=picture_form)
            return self.render_to_response(context)


    def get_object(self):
        # Call the superclass
        object = super(BrabEditView, self).get_object()
        # If necessary, modify the Brab object properties
        # then save it with object.save()
        # Return the object
        return object

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BrabEditView, self).get_context_data(**kwargs)
        # Add in some context dictionary value
        # context['book_list'] = Book.objects.all()
        return context

    def parse_tags(self, tags):
        tags = tags.lower()
        tags = re.split('; |, |,|;', tags)
        return tags

    def add_tag_records(self, tags, user_id, brab_id):
    #        Delete existing tag links
        Tag_to_brab.objects.filter(brab_id = brab_id).delete()
    #        Re-create tag links based on the updated information in the POST
        tag_count = 0
        for tag_text in tags:
            tag_count = tag_count + 1
            existing_tags = Tag.objects.filter(tag__exact=tag_text)
            if not existing_tags:
                tag_object = Tag(auth_user_id = user_id, tag = tag_text, visible = True)
                tag_object.save()
                if not Tag_to_brab.objects.filter(brab_id = brab_id, tag_id = tag_object.pk):
                    tag_link = Tag_to_brab(auth_user_id = user_id, brab_id = brab_id, tag_id = tag_object.pk)
                    tag_link.save()
            else:
                existing_tag = Tag.objects.get(tag__exact=tag_text)
                tag_link = Tag_to_brab(auth_user_id = user_id, brab_id = brab_id, tag_id = existing_tag.pk)
                tag_link.save()

        return tag_count

    def add_category_records(self, categories, user_id, brab_id):
    #        Delete existing category links
        Category_to_brab.objects.filter(brab_id = brab_id).delete()
    #        Re-create category links based on the updated information in the POST
        category_count = 0
        for categ_id in categories:
            category_count = category_count + 1
            if not Category_to_brab.objects.filter(brab_id = brab_id, category_id = categ_id):
                category_link = Category_to_brab(auth_user_id = user_id, brab_id = brab_id, category_id = categ_id)
                category_link.save()

        return category_count


class BrabListView(ListView):
    template_name = 'brabs/brab_list.html'
    paginate_by = 12

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        category_id = self.kwargs.get('category_id', None)
        tag_name = self.kwargs.get('tag_name', None)
        if self.request.path=="/envybrabs/":
            q = Brab.objects.filter(vote_to_brab__vote=4).filter(vote_to_brab__auth_user_id=self.request.user.id).distinct()
        elif self.request.path=="/fwbrabs/":
            fq=Follower_to_followee.objects.filter(follower_id=self.request.user.id)
            q = Brab.objects.filter(auth_user_id__in=fq).distinct()
        elif category_id:
            q = Brab.objects.filter(category_to_brab__category=category_id).distinct()
        elif tag_name:
            q = Brab.objects.filter(tag_to_brab__tag__tag=tag_name)
        else:
            if user_id:
                q =  Brab.objects.filter(auth_user_id=user_id)
            else:
                if self.request.GET:
                    search_for = self.request.GET["searchfor"]
                    if search_for:
                        search_for = re.split('; |, |,|;| ', search_for)
                        q = Brab.objects.filter(tag_to_brab__tag__tag__in=search_for)
                    else:
                        q = Brab.objects.filter(auth_user_id=self.request.user.id)
                else:
                    q = Brab.objects.filter(auth_user_id=self.request.user.id)
        return q

class Follower_to_followeeListView(LoggedInMixin, ListView):
        methods = ['get', 'post']
        template_name = 'brabs/followee_list.html'
        paginate_by = 12

        def post(self, request, *args, **kwargs):
            if 'SF' in request.POST:
                followee_id = request.POST['SF']
                Follower_to_followee.objects.filter(follower_id=self.request.user.id) \
                    .filter(followee_id = followee_id).update(deleted = 1)

            return redirect('/followees/')

        def get_queryset(self):
            # fq=Follower_to_followee.objects.filter(follower_id=self.request.user.id)
            fq = User.objects.filter(user_followees__follower=self.request.user.id).exclude(user_followees__deleted=1) \
                .annotate(brab_count=models.Count('brab'))
            return fq

        def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
            context = super(Follower_to_followeeListView, self).get_context_data(**kwargs)
            # Add in some context dictionary value
            # context['book_list'] = Book.objects.all()
            return context

class Followee_to_followerListView(LoggedInMixin, ListView):
    methods = ['get', 'post']
    template_name = 'brabs/follower_list.html'
    paginate_by = 12

    def post(self, request, *args, **kwargs):
        if 'SF' in request.POST:
            follower_id = request.POST['SF']
            Follower_to_followee.objects.filter(followee_id=self.request.user.id) \
                .filter(follower_id = follower_id).update(deleted = 1)

        return redirect('/followers/')

    def get_queryset(self):

        fq = User.objects.filter(user_followers__followee=self.request.user.id).exclude(user_followers__deleted=1) \
            .annotate(brab_count=models.Count('brab'))

        # fq = User.objects.filter(user_followers__followee=self.request.user.id).exclude(user_followers__deleted=1)

        return fq

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Followee_to_followerListView, self).get_context_data(**kwargs)
        # Add in some context dictionary value
        # context['book_list'] = Book.objects.all()
        return context
