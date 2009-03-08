# coding=UTF-8

from google.appengine.ext.db import GqlQuery
from google.appengine.api import users
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
import logging
import math
from models import Blog, Category, Archive, Comment, FriendlyURL
from forms import BlogForm, CommentForm, URLForm

def base_context():
    context = Context({
        'current_user':current_user(),
        'admin':admin(),
        'login_url':users.create_login_url('/blogs'),
        'logout_url':users.create_logout_url('/blogs'),
        'recent_comments':Comment.all().order('-date').fetch(5),
        'categories':Category.all(),
        'blogs_count':Blog.all().count(),
        'archives':Archive.all().order('-year').order('-month'),
        'friendlyURLs':FriendlyURL.all()
    })
    return context

def index(request):
    context = base_context()
    rpp = record_per_page()
    cur_page = 1
    if request != '' and request.method == 'POST':
        cur_page = int(request.POST['jumpPage'])
    else:
        cur_page = 1
    
    blogs_count = Blog.all().count()
    max_page = blogs_count / rpp
    temp2 = blogs_count % rpp
    if temp2 != 0:
        max_page = max_page + 1
        
    if cur_page > max_page or cur_page <= 0:
        cur_page = max_page
        blogs = Blog.all().order('-date').fetch(0); 
    else:
        blogs = Blog.all().order('-date').fetch(rpp, rpp * (cur_page - 1)); 

    context.cur_page = cur_page
    context.max_page = max_page
    context.action_mode = '/'
    context.range1 = range(1, max_page + 1)
    context.up_page=cur_page - 1
    context.down_page=cur_page + 1
    context.blogs = blogs
    template = loader.get_template('blogs/index.html')
    return HttpResponse(template.render(context))

def show_by_archive(request, year, month):
    context = base_context()
    rpp = record_per_page()
    cur_page = 1
    if request != '' and request.method == 'POST':
        cur_page = int(request.POST['jumpPage'])
    else:
        cur_page = 1
    
    blogs_count = Blog.all().filter('year', int(year)).filter('month', int(month)).count()
    max_page = blogs_count / rpp
    temp2 = blogs_count % rpp
    if temp2 != 0:
        max_page = max_page + 1
    
    if cur_page > max_page or cur_page <= 0:
        cur_page = max_page
        
    if cur_page > max_page:
        cur_page = max_page
        blogs = Blog.all().filter('year', int(year)).filter('month', int(month)).order('-date').fetch(0);
    else:
        blogs = Blog.all().filter('year', int(year)).filter('month', int(month)).order('-date').fetch(rpp, rpp * (cur_page - 1)); 
    
    context.cur_page = cur_page
    context.max_page = max_page
    context.action_mode = '/archive/' + year + '/' + month
    context.range1 = range(1, max_page + 1)
    context.up_page=cur_page - 1
    context.down_page=cur_page + 1
    context.blogs = blogs
    template = loader.get_template('blogs/index.html')
    return HttpResponse(template.render(context))

def show_by_category(request, key):
    context = base_context()
    rpp = record_per_page()
    cur_page = 1
    if request != '' and request.method == 'POST':
        cur_page = int(request.POST['jumpPage'])
    else:
        cur_page = 1
    
    blogs_count = Blog.all().filter('category', Category.get(key)).count()
    max_page = blogs_count / rpp
    temp2 = blogs_count % rpp
    if temp2 != 0:
        max_page = max_page + 1
    
    if cur_page > max_page or cur_page <= 0:
        cur_page = max_page
    
    if cur_page > max_page:
        cur_page = max_page
        blogs = Blog.all().filter('category', Category.get(key)).order('-date').fetch(0); 
    else:
        blogs = Blog.all().filter('category', Category.get(key)).order('-date').fetch(rpp, rpp * (cur_page - 1)); 
    context.cur_page = cur_page
    context.max_page = max_page
    context.action_mode = '/category/' + key + '/show'
    context.range1 = range(1, max_page + 1)
    context.up_page=cur_page - 1
    context.down_page=cur_page + 1
    context.blogs = blogs
    template = loader.get_template('blogs/index.html')
    return HttpResponse(template.render(context))

def show(request, key):
    context = base_context()
    blog = Blog.get(key)
    if not admin():
        blog.browsed_count += 1
        blog.put()
    comments = blog.comment_set.order('date')
    form = CommentForm()
    context.blog = blog
    context.comments = comments
    context.form = form
    template = loader.get_template('blogs/show.html')
    return HttpResponse(template.render(context))

def new(request):
    context = base_context()
    if not admin():
        return HttpResponseRedirect(users.create_login_url('/blogs'))
    if request.method == 'POST':
        form = BlogForm(request.POST)
    else:
        form = BlogForm()
    form.fields['category'].choices = [('', '请选择')] + [(category.key(), category.name) for category in Category.all()]
    context.form = form
    template = loader.get_template('blogs/new.html')
    return HttpResponse(template.render(context))

def create(request):
    if not admin():
        return HttpResponseRedirect(users.create_login_url('/blogs'))
    form = BlogForm(request.POST)
    form.fields['category'].choices = [('', '请选择')] + [(category.key(), category.name) for category in Category.all()]
    if form.is_valid():
        blog = Blog()
        blog.title = form.cleaned_data['title']
        blog.content = form.cleaned_data['content']
        if form.cleaned_data['category']:
            blog.category = Category.get(form.cleaned_data['category'])
        elif form.cleaned_data['user_tag']:
            blog.category = Category.get_or_insert(form.cleaned_data['user_tag'], name=form.cleaned_data['user_tag'])
        blog.create()
        return HttpResponseRedirect('/blogs')
    else:
        return new(request)

def edit(request, key):
    context = base_context()
    if not admin():
        return HttpResponseRedirect(users.create_login_url('/blogs'))
    blog = Blog.get(key)
    if request.method == 'POST':
        form = BlogForm(request.POST)
    else:
        form = BlogForm()
    form.fields['title'].initial = blog.title
    form.fields['content'].initial = blog.content
    form.fields['category'].choices = [('', '请选择')] + [(category.key(), category.name) for category in Category.all()]
    if blog.category:
        form.fields['category'].initial = blog.category.key()
    context.blog = blog
    context.form = form
    template = loader.get_template('blogs/edit.html')
    return HttpResponse(template.render(context))

def update(request, key):
    if not admin():
        return HttpResponseRedirect(users.create_login_url('/blogs'))
    form = BlogForm(request.POST)
    form.fields['category'].choices = [('', '请选择')] + [(category.key(), category.name) for category in Category.all()]
    if form.is_valid():
        blog = Blog.get(key)
        blog.title = form.cleaned_data['title']
        blog.content = form.cleaned_data['content']
        if form.cleaned_data['category']:
            blog.category = Category.get(form.cleaned_data['category'])
        elif form.cleaned_data['user_tag']:
            blog.category = Category.get_or_insert(form.cleaned_data['user_tag'], name=form.cleaned_data['user_tag'])
        else:
            blog.category = None
        blog.put()
        return HttpResponseRedirect('/blogs')
    else:
        return edit(request, key)

def delete(request, key):
    if not admin():
        return HttpResponseRedirect(users.create_login_url('/blogs'))
    blog = Blog.get(key)
    Comment.batch_delete(blog.comment_set)
    archive = Archive.all().filter('year', blog.year).filter('month', blog.month).fetch(1)
    archive[0].weblog_count -= 1
    archive[0].put()
    if archive[0].weblog_count == 0:
        archive[0].delete()
    blog.delete()
    return HttpResponseRedirect('/blogs')

def createComment(request, blog_key):
    if not current_user():
        return HttpResponseRedirect(users.create_login_url('/blogs'))
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = Comment()
        comment.blog = Blog.get(blog_key)
        comment.author = current_user()
        comment.content = form.cleaned_data['content']
        comment.put()
        context = Context({
            'blog':comment.blog,
            'comment':comment,
            'admin':admin(),
        })
        template = loader.get_template('blogs/_comment.html')
        return HttpResponse(template.render(context))
    else:
        return HttpResponse('')

def deleteComment(request, blog_key, comment_key):
    if not admin():
        return HttpResponseRedirect(users.create_login_url('/blogs'))
    comment = Comment.get(comment_key)
    comment.delete()
    return HttpResponseRedirect('/blog/' + blog_key + '/show')

def newURL(request):
    context = base_context()
    if not admin():
        return HttpResponseRedirect(users.create_login_url('/blogs'))
    if request.method == 'POST':
        form = URLForm(request.POST)
    else:
        form = URLForm()
    context.form = form
    template = loader.get_template('blogs/newURL.html')
    return HttpResponse(template.render(context))

def createURL(request):
    if not admin():
        return HttpResponseRedirect(users.create_login_url('/blogs'))
    form = URLForm(request.POST)
    if form.is_valid():
        friendlyURL = FriendlyURL()
        friendlyURL.name = form.cleaned_data['name']
        friendlyURL.URL = form.cleaned_data['URL']
        friendlyURL.put()
        return HttpResponseRedirect('/blogs')
    else:
        return newURL(request)

def editURL(request, key):
    context = base_context()
    if not admin():
        return HttpResponseRedirect(users.create_login_url('/blogs'))
    friendlyURL = FriendlyURL.get(key)
    if request.method == 'POST':
        form = URLForm(request.POST)
    else:
        form = URLForm()
    form.fields['name'].initial = friendlyURL.name  
    form.fields['URL'].initial = friendlyURL.URL
    context.friendlyURL = friendlyURL
    context.form = form
    template = loader.get_template('blogs/editURL.html')
    return HttpResponse(template.render(context))

def updateURL(request, key):
    if not admin():
        return HttpResponseRedirect(users.create_login_url('/blogs'))
    form = URLForm(request.POST)
    if form.is_valid():
        friendlyURL = FriendlyURL.get(key)
        friendlyURL.name = form.cleaned_data['name']
        friendlyURL.URL = form.cleaned_data['URL']
        friendlyURL.put()
        return HttpResponseRedirect('/blogs')
    else:
        return editURL(request, key)

def deleteURL(request, key):
    if not admin():
        return HttpResponseRedirect(users.create_login_url('/blogs'))
    friendlyURL = FriendlyURL.get(key)
    friendlyURL.delete()
    return HttpResponseRedirect('/blogs')

def admin():
    return users.is_current_user_admin()

def current_user():
    return users.get_current_user()def record_per_page():
    return 3

