# coding=UTF-8
from google.appengine.ext import db

class Configuration(db.Model):
	title=db.StringProperty()
	motto=db.StringProperty()

class FriendlyURL(db.Model):
    name=db.StringProperty()
    URL=db.URLProperty()

class Category(db.Model):
    name=db.StringProperty()

class Archive(db.Model):
    year=db.IntegerProperty()
    month=db.IntegerProperty()
    weblog_count=db.IntegerProperty()

class Blog(db.Model):
    title = db.StringProperty()
    category=db.ReferenceProperty(Category)
    content = db.TextProperty()
    browsed_count=db.IntegerProperty(default=0)
    date = db.DateTimeProperty(auto_now_add=True)
    year =db.IntegerProperty()
    month=db.IntegerProperty()
    
    def create(self):
        self.year=self.date.year
        self.month=self.date.month
        self.update_archive()
        self.put()
    
    def update_archive(self):
        m=self.date.month
        y=self.date.year
        archive=Archive.all().filter('month',m).filter('year',y).fetch(1)
        if archive==[]:
            archive=Archive(month=m,year=y,weblog_count=1)
            archive.put()
        else:
            archive[0].weblog_count+=1
            archive[0].put()

class Comment(db.Model):
    blog = db.ReferenceProperty(Blog)
    author = db.UserProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def batch_delete(self,comments):
        db.delete(comments)
    
