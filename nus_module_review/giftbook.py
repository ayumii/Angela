import urllib
import webapp2
import jinja2
import os
import datetime


from google.appengine.ext import db
from google.appengine.api import users

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
class Persons(db.Model):
  """Models a person identified by email"""
  email = db.StringProperty()
  username = db.StringProperty()
  faculty = db.StringProperty()
  gender = db.StringProperty()
  year = db.StringProperty()

class Items(db.Model):
  """Models an item with item_link, image_link, description, and date."""
  item_link = db.StringProperty()
  image_link = db.StringProperty()
  description = db.StringProperty(multiline=True) # pressing enter will not affect the result, descrip. allows /n  
  date = db.DateTimeProperty(auto_now_add=True) # add automatically upon calling the constructor for the entity. and the date is in GMT+0
    
class AddList(webapp2.RequestHandler):
  """ Add an item to the datastore """
  def post(self): #similar to pushing data
  # Retrieve person
    parent_key = db.Key.from_path('Persons', users.get_current_user().email()) #person -class represented as a string
    person = db.get(parent_key) #it will return the person object that is associated with the key called parent_key
    if person == None:
      newPerson = Persons(key_name=users.get_current_user().email())
      newPerson.put() #push object to store it in the database similar to vector.push_back()

    item = Items(parent=parent_key) #items=constructor, parent=parent_key, item=child
    item.item_link = self.request.get('item_url')  #note only under POST method then we can use self.request.get to retrieve info from user
    item.image_link = self.request.get('image_url')
    item.description = self.request.get('desc')

    # Only store an item if there is an image
    if item.image_link.rstrip() != '':
      item.put()
    self.redirect('/wishlist')

class Cors(webapp2.RequestHandler):
  """ Form for getting and displaying wishlist items. """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already

      # Retrieve person
      parent_key = db.Key.from_path('Persons', users.get_current_user().email())

      query = db.GqlQuery("SELECT * FROM Items WHERE ANCESTOR IS :1 ORDER BY date DESC", parent_key)

      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url), #host_url : default/main page of the webpage
        'items': query,
        } 

      template = jinja_environment.get_template('cors.html')
      self.response.out.write(template.render(template_values))
    
    else:
      self.redirect(self.request.host_url)
      
class WishList(webapp2.RequestHandler):
  """ Form for getting and displaying wishlist items. """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already

      # Retrieve person
      parent_key = db.Key.from_path('Persons', users.get_current_user().email())

      query = db.GqlQuery("SELECT * FROM Items WHERE ANCESTOR IS :1 ORDER BY date DESC", parent_key)

      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url), #host_url : default/main page of the webpage
        'items': query,
        } 

      template = jinja_environment.get_template('profile.html')
      self.response.out.write(template.render(template_values))
    
    else:
      self.redirect(self.request.host_url)

class WishListtwo(webapp2.RequestHandler):
  """ Form for getting and displaying wishlist items. """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already

      # Retrieve person
      parent_key = db.Key.from_path('Persons', users.get_current_user().email())

      query = db.GqlQuery("SELECT * FROM Items WHERE ANCESTOR IS :1 ORDER BY date DESC", parent_key)
      #ancestor is :1 means the first parameter passed is parent_key
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'items': query,
        } 

      template = jinja_environment.get_template('changeprofile.html')
      self.response.out.write(template.render(template_values))
    
    else:
      self.redirect(self.request.host_url)


class WishListthree(webapp2.RequestHandler):
  """ Form for getting and displaying wishlist items. """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already

      # Retrieve person
      parent_key = db.Key.from_path('Persons', users.get_current_user().email())

      query = db.GqlQuery("SELECT * FROM Items WHERE ANCESTOR IS :1 ORDER BY date DESC", parent_key)

      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'items': query,
        } 

      template = jinja_environment.get_template('createfirstprofile.html')
      self.response.out.write(template.render(template_values))
    
    else:
      self.redirect(self.request.host_url)

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

class Display(webapp2.RequestHandler):
  """ Displays search result """
  def post(self):

    target = self.request.get('email').rstrip()
    # Retrieve person
    parent_key = db.Key.from_path('Persons', target)

    query = db.GqlQuery("SELECT * FROM Items WHERE ANCESTOR IS :1 ORDER BY date DESC", parent_key)
      #yellow words used in html files
    template_values = {
      'user_mail': users.get_current_user().email(),
      'target_mail': target,
      'logout': users.create_logout_url(self.request.host_url),
      'items': query,
      } 
    template = jinja_environment.get_template('display.html')
    self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([('/giftbook', MainPage),
  ('/Login', Login),
  ('/cors', Cors),
  ('/profile', WishList),
  ('/changeprofile', WishListtwo),
  ('/createfirstprofile', WishListthree),
  ('/addR ', AddList),
  ('/search', Search),
  ('/display', Display)],
  debug=True)
#class Mainpage is mapped to the root URL (/) 