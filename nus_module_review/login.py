import webapp2

from google.appengine.api import users

class LoginHandler(webapp2.RequestHandler):
  """ Redirect users to NUS OpenId for login."""
  def get(self):
    continue_url = self.request.GET.get('continue')
    openid_url = self.request.GET.get('openid')
    if openid_url:
      self.redirect(users.create_login_url(continue_url, None, openid_url))
    else:    
      self.redirect(users.create_login_url(continue_url, None, federated_identity='https://openid.nus.edu.sg/'))

app = webapp2.WSGIApplication([('/_ah/login_required', LoginHandler)],
  debug=True)