from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView ,DetailView
from django.contrib.auth.models import User
from.models import *
from django.views.generic.edit import FormMixin
from django.core.exceptions import ValidationError
from datetime import datetime
from taggit.models import Tag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
# Create your views here.


class BlogList(ListView):
    model=Post
    paginate_by=4
    
    def get_queryset(self):
        name=self.request.GET.get('q','')
        #this is ture but when use Q to search  i u can search in two => ""title ,description"" 
        #if not u must write 2 or 3 line to search
        # object_list=Post.objects.filter(title__icontains=name)
        
        object_list=Post.objects.filter(Q(title__icontains=name)| 
                                        Q(description__icontains=name))
        return object_list
    
class BlogDetail(DetailView):
    model=Post
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["categories"]=Category.objects.all()
        context["tags"]=Tag.objects.all()
        current_post = self.object
        current_post_comment = get_object_or_404(Post, slug=self.kwargs['slug'])
        context["comments"] = AddComment.objects.filter(property=current_post_comment)
        # get last frist 3 post i was add except post iam in now 
        context["recent_posts"] = Post.objects.filter(~Q(id=current_post.id))[:3] 
        return context
    def post(self,request,*args, **kwargs):
        message=None
        if request.method=='POST':
            message=request.POST.get('message')
            commnet=AddComment.objects.create(
                user=request.user,
                property=self.get_object(),
                message=message,
                
                )
            commnet.save()
            return super().get(request, *args, **kwargs)


class PostByCategory(ListView):
    model=Post
    
    def get_queryset(self):
        slug=self.kwargs['slug']
        object_list=Post.objects.filter(Q(category__name__icontains=slug))
        return object_list

class PostByTags(ListView):
    model=Post
    
    def get_queryset(self):
        slug=self.kwargs['slug']
        object_list=Post.objects.filter(Q(tag__name__icontains=slug))
        return object_list