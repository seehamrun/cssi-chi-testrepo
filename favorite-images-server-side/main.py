import webapp2
import logging
import jinja2
import os
import json
import api

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch



class FavoriteUrl(ndb.Model):
    url = ndb.StringProperty()
    username = ndb.StringProperty()


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.info('current user is %s' % (user.nickname()))
        template = jinja_env.get_template('templates/index.html')
        data = {
          'user_nickname': user.nickname(),
          'logoutUrl': users.create_logout_url('/')
        }
        return self.response.write(template.render(data))


class AddFavoriteHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        logging.info('current user is %s' % (user.nickname()))
        requestUrl = self.request.get('url')
        logging.info('server saw a request to add %s to list of favorites' % (requestUrl))
        favoriteUrl = FavoriteUrl(url=requestUrl, username=user.nickname())
        favoriteUrl.put()


class ListFavoritesHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logging.info('current user is %s' % (user.nickname()))
        template = jinja_env.get_template('templates/favorites.html')
        data = {
          'favorites': FavoriteUrl.query(FavoriteUrl.username == user.nickname()).fetch(),
          'logoutUrl': users.create_logout_url('/'),
        }
        return self.response.write(template.render(data))

def queryGiphy(query):
    url = "http://api.giphy.com/v1/gifs/search?api_key=%s&q=%s&limit=%d"%(api.giphy_api_key, query, 1)
    response = json.loads(urlfetch.fetch(url).content)["data"]
    response = response[0]
    response = response["images"]
    response = response["downsized"]
    response = response["url"]
    return response

class GetImageHandler(webapp2.RequestHandler):
    def get(self):
        query = self.request.get('query')
        return self.response.write(queryGiphy(query))


app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/add_favorite', AddFavoriteHandler),
    ('/list_favorites', ListFavoritesHandler),
    ('/get_image', GetImageHandler)
], debug=True)
