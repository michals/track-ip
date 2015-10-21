import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        out = self.response.out
        try:
            server_name = self.request.server_name
            suffix = '.localhost' if server_name.endswith('localhost') else '.track-ip.appspot.com'
            hostname = server_name.rsplit(suffix, 1)[:-1][0]
            out.write(hostname)
            # now we print hostname, later we resolve it, and print ip
        except:
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
