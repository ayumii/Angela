import urllib
import webapp2
import jinja2
import os
import datetime
import time
import json
import urllib2
#import win32api

from datetime import datetime


#import cgi


from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.db import polymodel
#from google.appengine.api import images


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
  ratings = db.StringProperty()
  workload = db.StringProperty()
  diff = db.StringProperty()
  text = db.TextProperty() #allows text of more than 500 characters
  email = db.StringProperty()#identify user that wrote review
  date = db.DateTimeProperty(auto_now_add=True)
  checkr= db.IntegerProperty()
#to count the number of reviews for future use  
class CountReviews(db.
  Model):
  """Models the number of reviews written for each module"""
  code = db.StringProperty()
  count = db.IntegerProperty()

class Persons(db.Model):
  """Models a person identified by email"""
  email = db.StringProperty()
  username = db.StringProperty()
  faculty = db.StringProperty()
  gender = db.StringProperty()
  year = db.StringProperty()
  image = db.StringProperty()
  #image = db.BlobProperty()
  #image =('images',Field('picture', 'upload', uploadfield='picture_file') Field('picture_file', 'blob'))
  

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
    modcode = self.request.get('code')
    email = users.get_current_user().email()
    query = db.GqlQuery("SELECT * from ModuleReviews where code =:1 and email =:2", modcode, email)
    #self.response.out.write(query.code)
    #module = query.get()
    if query.count() == 1:
      #self.response.out.write(query.code)
      module = query.get()
      module.checkr = 1
      module.put()
      #self.redirect('/errorR')
      #win32api.MessageBox(0, 'hello', 'title')
    
    else:
     #query.count() == None:
      #self.response.out.write(query.code)
      module = ModuleReviews(code=self.request.get('code'),text=self.request.get('review')) #stores module in database
      module.text =  self.request.get('review')
      module.code = self.request.get('code')
      module.ratings = self.request.get('ratings')
      module.workload = self.request.get('workload')
      module.diff = self.request.get('diff')
      module.email = users.get_current_user().email()
      module.put()
      #self.redirect('/display')
    #searchcode = self.request.get("code")
    #count = CountReviews(key_name=self.request.get("code"))
    #query = db.GqlQuery("SELECT * FROM ModuleReviews WHERE code =:1 ",searchcode)
    #count.code = searchcode
    #count.count = query.count() 
    #count.put()
    #time.sleep(2)

    #template = jinja_environment.get_template('display.html')
    #self.response.out.write(template.render(template_values))

class viewR(webapp2.RequestHandler):
  """ View reviews of module that user search for """

  def get(self):

    user = users.get_current_user()
    if user:  # signed in already   
       
       searchcode = self.request.get('code')
       
       
       query = db.GqlQuery("SELECT * from ModuleReviews where code =:1", searchcode).fetch(limit= None,  deadline=60, offset=0, keys_only=False, projection=None, start_cursor=None, end_cursor=None)
      
       alist = []

       blist = []
       i = 0

       for module in query:
        alist.append( query[i] )
        query2 = db.GqlQuery("SELECT * from Persons where email =:1", alist[i].email).get()  
        blist.append( query2 )

        #count = db.GqlQuery("SELECT * from CountReviews where code =:1", searchcode).get()

        #if not count:
          #num = 0

        #else:
         #count.code = searchcode
         #count.count = query.count(searchcode)
         #count.put()
         #count.count += 1  
        
        i+=1

 
       #count = CountReviews(key_name=self.request.get("code"))
       
       #count = db.GqlQuery("SELECT * from CountReviews where code =:1", searchcode).fetch(limit= None,  deadline=60, offset=0, keys_only=False, projection=None, start_cursor=None, end_cursor=None)
       
       #count.code = searchcode
       #count.count = query.count(searchcode)
       #count.count += 1 
       #count.put()
       #count = db.GqlQuery("SELECT * from CountReviews where code =:1", searchcode).get()



    template_values = {
        'user_mail' : users.get_current_user().email(),
        'logout' : users.create_logout_url(self.request.host_url), #host_url : default/main page of the webpage
        'query2' : blist,  
        'query' : alist,
        'code': searchcode,
        'i' : i,
        #'count': count,
        } 
    
    template = jinja_environment.get_template('viewR.html')
    self.response.out.write(template.render(template_values))

  


class Profile(webapp2.RequestHandler):
  """ Form for getting and displaying wishlist items. """
  
  #def download():
    #return response.download(request, db)
  
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

    #image = images.resize(self.request.get('person_image'), 32, 32)
    #person.image = db.Blob(image)
    person.image = self.request.get('person_image')
    person.email = users.get_current_user().email()
    person.put()

  
    #if person.image:
      #self.response.headers['Content-Type'] = 'image/png'
      #self.response.out.write(person.image)
    #else:
      #self.response.out.write('No image')

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

class SearchGem(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('gem.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)  

class SearchSS(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('ss.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)  

class SearchBreadthandUE(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        } 
      template = jinja_environment.get_template('breadthandue.html')
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
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('fass.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)


class SearchFacultyDentistry(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('dentistry.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)

class SearchFacultyEngineering(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('engineering.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)

class SearchFacultyJmdp(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('jmdp.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)

class SearchFacultyLaw(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('law.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)


class SearchFacultyNfbd(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('nfbd.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)

class SearchFacultyBusiness(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('business.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)

class SearchFacultyComputing(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('computing.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)


class SearchFacultySde(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('sde.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)

class SearchFacultyScience(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('science.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)

class SearchFacultyUa(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('ua.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)

class SearchFacultyUsp(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('usp.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)

class SearchFacultyMedicine(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('medicine.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)

class SearchFacultyMusic(webapp2.RequestHandler):
  """ Display search page """
  def get(self):
    user = users.get_current_user()
    query = db.GqlQuery("SELECT * from CountReviews") 
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        'query': query,
        } 
      template = jinja_environment.get_template('music.html')
      self.response.out.write(template.render(template_values))
    else:
      self.redirect(self.request.host_url)
    
    


class Display(webapp2.RequestHandler):
  """ Displays reviews user has written """
  def get(self):

    useremail = users.get_current_user().email() 
    query = db.GqlQuery("SELECT * from ModuleReviews where email = :1", useremail)
    #query.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #query.date = query.date.replace(hour=(query.date.hour+8)%24)
    person = db.GqlQuery("SELECT * from Persons where email =:1", useremail ).get()

    #now=datetime.now()
    #dateandtime = str(now.day) + "/" + str(now.month) + "/" + str(now.year) + " " + str ((now.hour)+8) + ":" + str(now.minute) + ":" + str(now.second)




    template_values = {
      'user_mail': users.get_current_user().email(),
      #'target_mail': target,
      'logout': users.create_logout_url(self.request.host_url),
      'query': query,
      #'date' : query.date,
      'person' : person,
      #'dateandtime' : dateandtime,
      
    }
    

    template = jinja_environment.get_template('display.html')
    self.response.out.write(template.render(template_values))

    count = 1
    email = users.get_current_user().email()
    query = db.GqlQuery("SELECT * from ModuleReviews where checkr =:1 and email =:2", count, email)

    if query.count() == 1:
      module = query.get()
      module.checkr = None
      module.put()

  def post(self):

    useremail = users.get_current_user().email() 
    index = int(self.request.get("button") )
    query = db.GqlQuery("SELECT * from ModuleReviews where email = :1", useremail )
    #self.response.write(query[index].ratings) 
    query[index].delete() 
    time.sleep(2)

    self.redirect("/display")
    #template_values = {
      #'user_mail': users.get_current_user().email(),
      #'logout': users.create_logout_url(self.request.host_url),
      #'query': query
    #}
    
    #template = jinja_environment.get_template('display.html')
    #self.response.out.write(template.render(template_values))

class errorR(webapp2.RequestHandler):
  """ Displays reviews user has written """
  def get(self):

    #email = users.get_current_user().email() 
    #count = 1
    #query = db.GqlQuery("SELECT * from ModuleReviews where email = :1 and checkr =:2", email, count)
    #module = query.get()

    #if query.count() == 1:
    template_values = {
      'user_mail': users.get_current_user().email(),
      #'target_mail': target,
      'logout': users.create_logout_url(self.request.host_url),
      #'query': query,
    }

    template = jinja_environment.get_template('errorR.html')
    self.response.out.write(template.render(template_values))

    #else:
    #  self.redirect('/display')

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

#class GEM(webapp2.RequestHandler):
#  """ test """
#  def get(self):
#    user = users.get_current_user()
#    if user:  # signed in already
      #mod_info = urllib2.urlopen('http://nusmods.com/json/mod_info.json')
      #js = json.load(mod_info)
      #mod = js['cors']
#      json_data=open("mod_info")
#      data = json.load(json_data)
#      template_values = {
#        'js': data,
#        }
#        template = jinja_environment.get_template('GEM.html')
#        self.response.out.write(template.render(template_values))
    
#    else:
#      self.redirect(self.request.host_url)

        

class Trypeeps(webapp2.RequestHandler):
  """testing"""
  def get(self):
    user = users.get_current_user()
    if user:  # signed in already
      template_values = {
        'user_mail': users.get_current_user().email(),
        'logout': users.create_logout_url(self.request.host_url),
        
        } 
      template = jinja_environment.get_template('trypeeps.html')
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
  ('/gem', SearchGem),
  ('/ss', SearchSS),
  ('/breadthandue', SearchBreadthandUE),
  ('/searchfaculty', SearchFaculty),
  ('/fass',SearchFacultyFass),
  ('/dentistry', SearchFacultyDentistry),
  ('/engineering', SearchFacultyEngineering),
  ('/jmdp', SearchFacultyJmdp),
  ('/law', SearchFacultyLaw),
  ('/nfbd', SearchFacultyNfbd),
  ('/business', SearchFacultyBusiness),
  ('/computing', SearchFacultyComputing),
  ('/sde', SearchFacultySde),
  ('/science', SearchFacultyScience),
  ('/ua', SearchFacultyUa),
  ('/usp', SearchFacultyUsp),
  ('/medicine', SearchFacultyMedicine),
  ('/music', SearchFacultyMusic),
  ('/display', Display),
  ('/errorR', errorR),
  ('/trypeeps',Trypeeps)],
  debug=True)
#class Mainpage is mapped to the root URL (/) 