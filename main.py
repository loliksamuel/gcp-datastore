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


import webapp2
from google.appengine.ext import ndb
#from google.cloud import ndb
#from google.cloud import datastore
#import google.cloud.exceptions
import random


class Score(ndb.Model):
    ##score     = ndb.IntegerProperty()
    ##timestamp = ndb.DateTimeProperty(auto_now_add=True)
    key       = ndb.StringProperty()
    value     = ndb.StringProperty()


class Storage():
    def score_key(self):
        return ndb.Key('Score', 'Store')

    def populate(self, key, value):
        new_score = Score(parent=self.score_key())
        new_score.key = key#+random.randint(1, 1234)
        new_score.value = value#+random.randint(1, 1234)
        new_score.put()

    def get_value(self, key):
        score_query = Score.query(ancestor=key)#.order(-Score.timestamp)
        return score_query.get().value

class MainHandler(webapp2.RequestHandler):
    def get(self):
        print ('populating datastore !')
        storage = Storage()
        storage.populate("key2", "value2")
        #score = storage.get_value("key2")
        #query = storage.query(Score.key == "key2")

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('populating db key value with key2, value2 !')


class GetHandler(webapp2.RequestHandler):
    def get(self):
        print ('gettt')
        variable_name = self.request.get('name')
        print ('variable_name='+variable_name)
        k = ndb.Key(urlsafe=variable_name)
        v = k.get()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('the value of the variable variable_name '+variable_name+' is '+v+'.')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('get !')

    def get_key(client):
        # [START datastore_named_key]
        #client = datastore.Client()#"project_id")
        key = client.key('Task', 'sample_task')
        # [END datastore_named_key]

        return key

class SetHandler(webapp2.RequestHandler):
    def get(self):

        print ('/set?name=n&value=v')
        variable_name  = self.request.get('name')
        variable_value = self.request.get('value')

        storage = Storage()
        storage.populate(variable_name, variable_value)

        # Score.key = variable_name
        # Score.value = variable_value

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('/set?name=n&value=v : '+variable_name +"="+variable_value)
        self.response.headers['Content-Type'] = 'text/plain'
        #self.response.write('set !')


class UnsetHandler(webapp2.RequestHandler):
    def get(self):
        print ('/unset')
        variable_name = self.request.get('name')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('/unset?name='+variable_name)


class NumEqualToHandler(webapp2.RequestHandler):
    def get(self):
        print ('/numequalto?value=val1')
        variable_value = self.request.get('value')
        query = Score.query(Score.value == variable_value)
        counter = query.count()
        # variable_value = 0
        # query = client.query(kind='Task')
        # query.add_filter('start', '=', variable_value)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('/numequalto  found this value '+counter+' times')


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


class EndHandler(webapp2.RequestHandler):
    def get(self):
        print ('EndHandler')
        kind_list = ['Task']

        #namespace_manager.set_namespace(namespace) # will set to the namespace provided

        for a_kind in kind_list:
            # will fetch keys of all objects in that kind
            kind_keys = a_kind.gql("").fetch(keys_only = True)
            # will delete all the keys at once
            ndb.delete_multi(kind_keys)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('EndHandler !')



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


