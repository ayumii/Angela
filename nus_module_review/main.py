import urllib
import webapp2
import jinja2
import os
import datetime


from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.db import polymodel

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

# This part for the front page

class MainPage(webapp2.RequestHandler):
  """ Front page for those logged in """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('frontuser.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect('/')

class Login(webapp2.RequestHandler):
  def get(self): #similar to pulling existing data
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'home': self.request.host_url,
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        }
      template = jinja_environment.get_template('frontuser.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(users.create_login_url(federated_identity='https://openid.nus.edu.sg/'))

# Datastore definitions
class ModuleReviews(db.Model):  
  """Models a module with all its attributes including its reviews"""
  facname = db.StringProperty()
  code = db.StringProperty()
  text = db.TextProperty() #allows text of more than 500 characters
  email = db.StringProperty()#identify user that wrote review
  date = db.DateTimeProperty(auto_now_add=True)

#to count the number of reviews for future use  
#class CountReviews(db.Model):
  #"""Models the number of reviews written for each module"""
  #code = db.StringProperty()
  #count = db.IntegerProperty()

class Persons(db.Model):
  """Models a person identified by email"""
  email = db.StringProperty()
  username = db.StringProperty()
  faculty = db.StringProperty()
  gender = db.StringProperty()
  year = db.StringProperty()
  image = db.StringProperty()

class AddR(webapp2.RequestHandler):
  """ Add an item to the datastore """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url), #host_url : default/main page of the webpage
        } 

      template = jinja_environment.get_template('addR.html')
      self.response.out.write(template.render(template_values))

  def post(self):
    module = ModuleReviews(code=self.request.get("code"),text=self.request.get("review")) #stores module in database
    module.text =  self.request.get("review")
    module.code = self.request.get("code")
    module.email = users.get_current_user().email()
    module.put()
    
    #searchcode = self.request.get("code")
    #count = CountReviews(key_name=self.request.get("code"))
    #query = db.GqlQuery("SELECT * FROM ModuleReviews WHERE code =:1 ",searchcode)
    #count.code = searchcode
    #count.count = query.count() 
    #count.put()
    self.redirect('/display')


class viewR(webapp2.RequestHandler):
  """ View reviews of module that user search for """
  def post(self):
    user = users.get_current_user()
    if user:  # signed in already

       searchcode = self.request.get('code')
       query = db.GqlQuery("SELECT * from ModuleReviews where code =:1", searchcode).get()
       query2 = db.GqlQuery("SELECT * from Persons where email =:1", query.email)
       #count = CountReviews(key_name=self.request.get("code"))
       #count.code = searchcode
       #count.count = query.count() 
       #count.put()
       #query2 = db.GqlQuery("SELECT * FROM CountReviews WHERE code =:1 ",searchcode)

    template_values = {
        'user_mail' : users.get_current_user().email(),
        'logout' : users.create_logout_url(self.request.host_url), #host_url : default/main page of the webpage
       # 'query' : query  
        'query2' : query2
        } 
    
    template = jinja_environment.get_template('viewR.html')
    self.response.out.write(template.render(template_values))


class Profile(webapp2.RequestHandler):
  """ Form for getting and displaying wishlist items. """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already

      # Retrieve person

      parent_key = db.Key.from_path('Persons', users.get_current_user().email())
      query2= db.get(parent_key)
      #query2 = db.GqlQuery("SELECT * FROM Items WHERE ANCESTOR IS :1 ORDER BY date DESC", parent_key)
      #query2 = db.GqlQuery("SELECT * FROM Persons WHERE ANCESTOR IS :1 ORDER BY date DESC", parent_key)
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url), #host_url : default/main page of the webpage
        'query2' : query2,
        #'items': query,
        #'person_name': query2.username,
        #'person_year' : query2.year,
        #'person_sex' : query2.gender,
        #'person_fac' : query2.faculty
        } 

      template = jinja_environment.get_template('profile.html')
      self.response.out.write(template.render(template_values))
    
    else:
      self.redirect(self.request.host_url)

class ChangeProfile(webapp2.RequestHandler):
  """ Form for getting and displaying wishlist items. """
  def get(self):
    
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 

      template = jinja_environment.get_template('changeprofile.html')
      self.response.out.write(template.render(template_values))
    
    else:
      self.redirect(self.request.host_url)

  def post(self): 
   
    user = users.get_current_user()
    if user:  # signed in already

      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
    parent_key = db.Key.from_path('Persons', users.get_current_user().email()) #person -class represented as a string
    person = db.get(parent_key) #it will return the person object that is associated with the key called parent_key

    #if person == None:
      #person = Persons(key_name=users.get_current_user().email())
      #person.put()  #push object to store it in the database similar to vector.push_back()

    #person = Persons(parent=parent_key) #items=constructor, parent=parent_key, item=child
    person = Persons(key_name=users.get_current_user().email())
    person.username = self.request.get('person_name')  #note only under POST method then we can use self.request.get to retrieve info from user
    person.year = self.request.get('person_year')
    person.gender = self.request.get('person_sex')
    person.faculty = self.request.get('person_fac')
    person.image = self.request.get('person_image')
    person.email = users.get_current_user().email()
    person.put()

    self.redirect('/profile')
        

class Search(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('search.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)     


class SearchFaculty(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('searchfaculty.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)

class SearchFacultyFass(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('fass.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)

class Display(webapp2.RequestHandler):
  """ Displays reviews user has written """
  def get(self):

    useremail = users.get_current_user().email() 
    query = db.GqlQuery("SELECT * from ModuleReviews where email = :1", useremail )

    template_values = {
      'user_mail': users.get_current_user().email(),
      #'target_mail': target,
      'logout': users.create_logout_url(self.request.host_url),
      'query': query
    }
    

    template = jinja_environment.get_template('display.html')
    self.response.out.write(template.render(template_values))

    
class Construction(webapp2.RequestHandler):
  """ webpage under construction """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 

      template = jinja_environment.get_template('construction.html')
      self.response.out.write(template.render(template_values))
    
    else:
      self.redirect(self.request.host_url)



app = webapp2.WSGIApplication([('/', MainPage),
  ('/Login', Login),
  ('/profile', Profile),
  ('/changeprofile', ChangeProfile),
  ('/addR', AddR),
  ('/viewR',viewR),
  ('/search', Search),
  ('/searchfaculty', SearchFaculty),
  ('/fass',SearchFacultyFass),
  ('/display', Display),
  ('/construction', Construction)],
  debug=True)
#class Mainpage is mapped to the root URL (/) 