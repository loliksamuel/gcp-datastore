# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#gcloud projects create dbkeyvalue
#gcloud config set project dbkeyvalue
#gcloud app deploy
#https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.ext.ndb.query

import webapp2
from google.appengine.ext import ndb
#from google.cloud import ndb
#from google.cloud import datastore
#import google.cloud.exceptions
import random


class KeyVal(ndb.Model):
    ##score     = ndb.IntegerProperty()
    ##timestamp = ndb.DateTimeProperty(auto_now_add=True)
    name       = ndb.StringProperty()
    value      = ndb.StringProperty()
    enabled    = ndb.BooleanProperty()


class Storage():
    def score_key(self):
        return ndb.Key('KeyVal', 'KeyVal')

    def populate(self, name, value, enabled):
        key_val       = KeyVal(parent=self.score_key())
        key_val.name    = name#+random.randint(1, 1234)
        key_val.value   = value#+random.randint(1, 1234)
        key_val.enabled = enabled#+random.randint(1, 1234)
        key_val.put()

    def get_value(self, key):
        #score_query = Score.query(ancestor=key)#.order(-Score.timestamp)
        score_query = KeyVal.query(kind='Score')#.order(-Score.timestamp)
        return score_query.get().value





class MainHandler(webapp2.RequestHandler):
    def get(self):
        print ('main! populating datastore !')
        storage = Storage()
        storage.populate("name", "value", False)
        #score = storage.get_value("key2")
        #query = storage.query(Score.key == "key2")

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('populating db key value with key2, value2 !')


class SetHandler(webapp2.RequestHandler):
    def get(self):

        print ('/set?name=n&value=v')
        variable_name  = self.request.get('name')
        variable_value = self.request.get('value')

        storage = Storage()
        storage.populate(variable_name, variable_value, True)

        # Score.key = variable_name
        # Score.value = variable_value

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('/set?name=n&value=v : '+variable_name +"="+variable_value)
        self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('set !')


class GetHandler(webapp2.RequestHandler):
    def get(self):
        print ('/get?name=n')
        variable_name = self.request.get('name')
        print ('variable_name='+variable_name)
        #v = variable_name.get()
        #try:
        list = KeyVal.query().filter(ndb.AND(KeyVal.name == variable_name, KeyVal.enabled == True))
        keyval = list.get()
        #     k = ndb.Key(urlsafe=variable_name)
        #     if not k:
        #         v = None
        #     else:
        #         v = k.get()
        # except TypeError, e1 :
        #     v = None
        #     #raise ValueError(e1.message)
        # except Exception, e2:
        #     v = None
        #     # if e2.__class__.__name__ == 'ProtocolBufferDecodeError':
        #     #     raise ValueError(e2.message)
        #     # else:
        #     #     raise ValueError(e2.message)


        self.response.headers['Content-Type'] = 'text/plain'
        if keyval == None:
            self.response.write('{0}\n'.format(keyval))
        else:
            self.response.write('{0}\n'.format(keyval.value))
        #for keyval in list:
         #   self.response.write('{0}\n'.format(keyval.value))
        #self.response.write('k =  {0}'.format([k]))

        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('get !')


class UnsetHandler(webapp2.RequestHandler):
    def get(self):
        print ('/unset?name=n')
        variable_name = self.request.get('name')

        #query = KeyVal.query().filter(KeyVal.key == variable_name)
        #keyval = query.get()
        #keyval.key.delete()
        list = KeyVal.query().filter(ndb.AND(KeyVal.name == variable_name, KeyVal.enabled == True))
        keyval = list.get()
        keyval.enabled = False
        keyval.put()
        # list = KeyVal.query().filter(KeyVal.name == variable_name)
        # for l in list.fetch(limit = 1):
        #     l.key.delete()

        #keyval = ndb.Key("KeyVal", variable_name).get()
        #keyval.key.delete()



        # for keyval in list:
        #     #self.response.write('{0}\n'.format(keyval.value))
        #     keyval.key.delete()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('/unset?name='+variable_name +"   deleted!")


class NumEqualToHandler(webapp2.RequestHandler):
    def get(self):
        print ('/numequalto?value=val1')
        variable_value = self.request.get('value')
        list = KeyVal.query().filter(ndb.AND(KeyVal.value == variable_value, KeyVal.enabled == True))
        #keyval = list.get()
        counter = list.count()
        # variable_value = 0
        # query = client.query(kind='Task')
        # query.add_filter('start', '=', variable_value)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('/numequalto  found this value {0}'.format(counter)+' times')


class UndoHandler(webapp2.RequestHandler):
    def get(self):
        print ('UndoHandler')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('UndoHandler !')


class RedoHandler(webapp2.RequestHandler):
    def get(self):
        print ('RedoHandler')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('RedoHandler !')

# Exit the program.
# remove all your data from the application (clean all the Datastore entities).
# Print CLEANED when done.
class EndHandler(webapp2.RequestHandler):
    def get(self):
        print ('/end')
        ndb.delete_multi(KeyVal.query().fetch(keys_only=True))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('db CLEANED !')




        # app = webapp2.WSGIApplication([
#     ('/', MainPage),
# ], debug=True)

# class NewHandler(webapp2.RequestHandler):
#     def get(self):
#         client = datastore.Client('dbkeyvalue')
#         print ('NewHandler')
#         task = datastore.Entity(client.key('Tasks'))
#         task.update({
#             'category': 'Personal',
#             'done': False,
#             'priority': 4,
#             'description': 'Learn Cloud Datastore'
#         })
#
#         self.response.headers['Content-Type'] = 'text/plain'
#         self.response.write('New Entity created !')


app = webapp2.WSGIApplication([
    ('/'     ,	MainHandler),
    ('/get'  ,	GetHandler),
    ('/set'  , 	SetHandler),
    ('/unset',  UnsetHandler),
    ('/numequalto', NumEqualToHandler),
    ('/undo' , 	 UndoHandler),
    ('/redo' , 	 RedoHandler),
    ('/end'  ,   EndHandler),
    #('/new'  ,   NewHandler),
     ], debug=False)


