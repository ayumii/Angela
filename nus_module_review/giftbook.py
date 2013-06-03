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
      self.response.out.write('Hello, '+ template.render(template_values))
    else:
      self.redirect('/')

class Login(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'home': self.request.host_url,
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        }
      template = jinja_environment.get_template('frontuser.html')
      self.response.out.write('Hello, '+template.render(template_values))
    else:
      self.redirect(users.create_login_url( federated_identity='https://openid.nus.edu.sg/'))

# Datastore definitions
class Persons(db.Model):
  """Models a person identified by email"""
  email = db.StringProperty()
  
class Items(db.Model):
  """Models an item with item_link, image_link, description, and date."""
  item_link = db.StringProperty()
  image_link = db.StringProperty()
  description = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
 
class AddList(webapp2.RequestHandler):
  """ Add an item to the datastore """
  def post(self):
    # Retrieve person
    parent_key = db.Key.from_path('Persons', users.get_current_user().email())
    person = db.get(parent_key)
    if person == None:
      newPerson = Persons(key_name=users.get_current_user().email())
      newPerson.put()

    item = Items(parent=parent_key)
    item.item_link = self.request.get('item_url')
    item.image_link = self.request.get('image_url')
    item.description = self.request.get('desc')

    # Only store an item if there is an image
    if item.image_link.rstrip() != '':
      item.put()
    self.redirect('/wishlist')
 
class WishList(webapp2.RequestHandler):
  """ Form for getting and displaying wishlist items. """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already

      # Retrieve person
      parent_key = db.Key.from_path('Persons', users.get_current_user().email())

      query = db.GqlQuery("SELECT * "
                          "FROM Items "
                          "WHERE ANCESTOR IS :1 "
                          "ORDER BY date DESC",
                          parent_key)

      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'items': query,
        } 

      template = jinja_environment.get_template('wishlist.html')
      self.response.out.write('Hello, '+template.render(template_values))
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

    query = db.GqlQuery("SELECT * "
                        "FROM Items "
                        "WHERE ANCESTOR IS :1 "
                        "ORDER BY date DESC",
                        parent_key)

    template_values = {
      'user_mail': users.get_current_user().email(),
      'target_mail': target,
      'logout': users.create_logout_url(self.request.host_url),
      'items': query,
      } 
    template = jinja_environment.get_template('display.html')
    self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([('/giftbook', MainPage),
                               ('/wishlist', WishList),
                               ('/addlist', AddList),
                               ('/search', Search),
                               ('/display', Display)],
                              debug=True)
#class Mainpage is mapped to the root URL (/) 