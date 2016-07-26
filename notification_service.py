import webapp2

from google.appengine.ext import ndb

DEFAULT_LOG = "default_log"

class LogEntry(ndb.Model):
    """A main model for representing log entry for this request"""
    request_body = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

def log_key(log_name=DEFAULT_LOG):
    """Constructs a Datastore key for a LogEntry entity.

       Use log_name as the key.
    """
    return ndb.Key('Log', log_name)
    

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('(Get) Hello, World!!')

    def post(self):
        # Get information from request
        headers = self.request.headers
        body = self.request.body
        if 'log_name' in headers:
            log_name = headers['log_name']
        else:
            log_name = DEFAULT_LOG

        # Create log entry
        log_entry = LogEntry(parent=log_key(log_name))
        log_entry.request_body = body
        log_entry.put()

        # Create response
        response = "[Log %s]: %s" % (log_name, body)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(response)
        self.response.write('---')
        self.response.write(headers)

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
