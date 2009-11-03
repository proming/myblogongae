
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^t1/', include('t1.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),\
    (r'^$','blogs.views.index'),
    (r'^blogs$','blogs.views.index'),
    (r'^category/(?P<key>.+)/show$','blogs.views.show_by_category'),
    (r'^blog/new$','blogs.views.new'),
    (r'^blog/create$','blogs.views.create'),
    (r'^blog/(?P<key>.+)/edit$','blogs.views.edit'),
    (r'^blog/(?P<key>.+)/update$','blogs.views.update'),
    (r'^blog/(?P<key>.+)/delete$','blogs.views.delete'),
    (r'^blog/(?P<key>.+)/show$','blogs.views.show'),
    (r'^blog/(?P<blog_key>.+)/comment/create$','blogs.views.createComment'),
    (r'^blog/(?P<blog_key>.+)/comment/(?P<comment_key>.+)/delete$','blogs.views.deleteComment'),
    (r'^url/new$','blogs.views.newURL'),
    (r'^url/create$','blogs.views.createURL'),
    (r'^url/(?P<key>.+)/edit$','blogs.views.editURL'),
    (r'^url/(?P<key>.+)/update$','blogs.views.updateURL'),
    (r'^url/(?P<key>.+)/delete$','blogs.views.deleteURL'),
	(r'^configuration/new$','blogs.views.newConfiguration'),
    (r'^configuration/create$','blogs.views.createConfiguration'),
    (r'^configuration/(?P<key>.+)/edit$','blogs.views.editConfiguration'),
    (r'^configuration/(?P<key>.+)/update$','blogs.views.updateConfiguration'),
    (r'^archive/(?P<year>\d+)/(?P<month>\d+)$','blogs.views.show_by_archive'),
)
