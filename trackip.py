import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users


class Host(ndb.Model):
    ''' This kind will map hostname to it's ip '''
    ip = ndb.StringProperty()
    code = ndb.TextProperty() # no need to query by code, unindexed

    @property
    def name(self):
        ''' host name is used as entity key. Cannot be changed. '''
        return self.key.string_id()

    @classmethod
    def get_by_name(cls, name):
        ''' get entity by host name '''
        return ndb.Key(cls, name).get()


class Profile(ndb.Model):
    ''' user profile having own hosts. We use Users.user_id() as a key. '''
    hostkeys = ndb.KeyProperty(repeated=True, kind=Host)

    @classmethod
    def get_by_user(cls, user):
        return cls.get_by_id(user.user_id())

    @property
    def hosts(self):
        return ndb.get_multi(self.hostnames)


class MainPage(webapp2.RequestHandler):
    def get(self):
        out = self.response.out
        server_name = self.request.server_name
        suffix = '.localhost' if server_name.endswith('localhost') else '.track-ip.appspot.com'
        hostname = server_name.rsplit(suffix, 1)[:-1]
        if hostname:
            host = Host.get_by_name(hostname[0])
            if not host:
               self.error(403)
            else:
                self.response.headers['Content-Type'] = 'text/plain'
                out.write(host.ip)
        else:
            user = users.get_current_user()
            self.response.headers['Content-Type'] = 'text/html'
            if user:
                prof = Profile.get_by_user(user)
                if not prof:
                    prof = Profile(id=user.user_id())
                    prof.put()
                greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
            else:
                greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))
            out.write('<html><body>%s</body></html>' % greeting)

class SaveIpPage(webapp2.RequestHandler):
    def get(self, hostname, code):
        self.response.headers['Content-Type'] = 'text/plain'
        out = self.response.out
        ip_to_save = self.request.remote_addr
        out.write('{ip_to_save} for {hostname}... '.format(**locals()))
        host = Host.get_by_name(hostname)
        if not host:
            # not in datastore, lets create it!
            host = Host(id=hostname, ip=ip_to_save)
            host.code = code
            out.write('creating new host... ')
            host.put()
            out.write('OK')
        else:
            # host in datastore, let's update ip
            out.write('updating ip... ')
            if host.code == code:
                if host.ip != ip_to_save:
                    host.ip = ip_to_save
                    host.put()
                    out.write('OK')
                else:
                    out.write('no change. OK')
            else:
                self.error(403)
                return;

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/ip/save/(\w+)/(\w+)', SaveIpPage),
], debug=True)
