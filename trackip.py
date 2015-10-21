import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(':-)')

class SaveIpPage(webapp2.RequestHandler):
    def get(self, hostname, code):
        self.response.headers['Content-Type'] = 'text/plain'
        out = self.response.out
        ip_to_save = self.request.remote_addr
        out.write('saving {ip_to_save} for {hostname} if {code} is correct...'.format(**locals()))
        try:
            # real save goes here
            out.write('OK')
        except:
            out.write('ERROR')

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/ip/save/(\w+)/(\w+)', SaveIpPage),
], debug=True)
