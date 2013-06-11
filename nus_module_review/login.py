import webapp2
import jinja2
import os

from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

class LoginHandler(webapp2.RequestHandler):
  """ Redirect users to NUS OpenId for login."""
  def get(self):
    continue_url = self.request.GET.get('continue')
    openid_url = self.request.GET.get('openid')
    if openid_url:
      self.redirect(users.create_login_url(continue_url, None, openid_url))
    else:    
    self.redirect(users.create_login_url(continue_url, None, federated_identity='https://openid.nus.edu.sg/')) 

#class LoginHandler(webapp2.RequestHandler):
  #""" Redirect users to different OpenId platforms for login."""
  #def get(self):
    #continue_url = self.request.GET.get('continue')
    #openid_url = self.request.GET.get('openid')
    #if openid_url:
      #if openid_url == 'NUS':
        #self.redirect(users.create_login_url(continue_url, None, federated_identity='https://openid.nus.edu.sg/'))
      #elif openid_url == 'Facebook':
        #self.redirect(users.create_login_url(continue_url, None, federated_identity='#'))
      #elif openid_url == 'Google':
        #self.redirect(users.create_login_url(continue_url, None ,federated_identity='https://www.google.com/accounts/o8/id'))
      #else:
        #self.redirect(users.create_login_url(continue_url, None, federated_identity='https://openid.nus.edu.sg/'))
    #else:    
      #self.redirect(users.create_login_url(continue_url, None, federated_identity='https://openid.nus.edu.sg/'))

app = webapp2.WSGIApplication([('/_ah/login_required', LoginHandler)],
                              debug=True)