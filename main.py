# gcloud projects create dbkeyvalue
# gcloud config set project dbkeyvalue
# gcloud app deploy
# https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.ext.ndb.query

import webapp2
from google.appengine.ext import ndb
import config
# from google.cloud import datastore
# import google.cloud.exceptions


class KeyVal(ndb.Model):
    # timestamp = ndb.DateTimeProperty(auto_now_add=True)
    name = ndb.StringProperty()
    value = ndb.StringProperty()
    enabled = ndb.BooleanProperty()


class Storage():
    @staticmethod
    def score_key():
        return ndb.Key('KeyVal', 'KeyVal')

    def populate(self, name, value, enabled):
        elements = KeyVal.query().filter(KeyVal.name == name)
        if elements.count() == 0:
            key_val = KeyVal(parent=self.score_key())
        else:
            key_val = elements.get()

        key_val.name = name  # +random.randint(1, 1234)
        key_val.value = value  # +random.randint(1, 1234)
        key_val.enabled = enabled  # +random.randint(1, 1234)
        key_val.put()

    @staticmethod
    def get_value(key):
        # score_query = Score.query(ancestor=key)#.order(-Score.timestamp)
        score_query = KeyVal.query(kind='Score')  # .order(-Score.timestamp)
        return score_query.get().value


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('main !')


class GetHandler(webapp2.RequestHandler):
    def get(self):
        print ('/get?name=n')
        variable_name = self.request.get('name')
        print ('variable_name=' + variable_name)
        elements = KeyVal.query().filter(ndb.AND(KeyVal.name == variable_name, KeyVal.enabled == True))
        element = elements.get()

        self.response.headers['Content-Type'] = 'text/plain'
        if element is None:
            self.response.write('{0}\n'.format(element))
        else:
            self.response.write('{0}\n'.format(element.value))


class SetHandler(webapp2.RequestHandler):
    def get(self):
        print ('/set?name=n&value=v')
        variable_name = self.request.get('name')
        variable_value = self.request.get('value')
        storage = Storage()
        storage.populate(variable_name, variable_value, True)
        self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write('/set?name=n&value=v : '+variable_name +"="+variable_value)
        self.response.write(variable_name + " = " + variable_value)
        config.history_index += 1
        config.history_list.append((variable_name, variable_value, True))


class UnsetHandler(webapp2.RequestHandler):
    def get(self):
        print ('/unset?name=n')
        variable_name = self.request.get('name')

        elements = KeyVal.query().filter(ndb.AND(KeyVal.name == variable_name, KeyVal.enabled == True))
        if elements.count() > 0:
            element = elements.get()
            element.enabled = False
            element.put()
        self.response.headers['Content-Type'] = 'text/plain'
        # self.response.write('/unset?name='+variable_name +"   deleted!")
        self.response.write(variable_name + " = None")


class UndoHandler(webapp2.RequestHandler):
    def get(self):
        """Undo a command if there is a command that can be undone.
        Update the history position with correct index, for  further UNDOs or REDOs """
        print ('/undo')
        self.response.headers['Content-Type'] = 'text/plain'

        if config.history_index > -1:
            state_curr = config.history_list[config.history_index]
            storage = Storage()
            if config.history_index < 1:
                storage.populate(state_curr[0], state_curr[1], False)
                self.response.write(state_curr[0] + " = None")  # +(not state_curr[2]))
                config.history_index -= 1
            else:
                config.history_index -= 1
                state_prev = config.history_list[config.history_index]

                if state_curr[0] == state_prev[0]:
                    storage.populate(state_prev[0], state_prev[1], state_prev[2])
                    self.response.write(state_prev[0] + " = " + state_prev[1])
                else:
                    storage.populate(state_curr[0], state_curr[1], False)
                    config.history_list.remove(state_curr)
                    self.response.write(state_curr[0] + " = None")  # +(not state_curr[2]))

            self.response.write(' \ncurrent index:{0}'.format(config.history_index))

        else:
            self.response.write('NO COMMANDS')


class RedoHandler(webapp2.RequestHandler):
    def get(self):
        print ('/redo')
        self.response.headers['Content-Type'] = 'text/plain'
        if config.history_index + 1 < len(config.history_list):
            config.history_index += 1
            state = config.history_list[config.history_index]
            storage = Storage()
            storage.populate(state[0], state[1], state[2])
            self.response.write(state[0] + " = " + state[1])
            self.response.write(' \ncurrent index:{0}'.format(config.history_index))

        else:
            self.response.write('NO COMMANDS')


class HistoryShowHandler(webapp2.RequestHandler):
    def get(self):
        """Return all records in the History list"""
        print ('/historyshow')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(config.history_list)
        self.response.write(' \ncurrent index:{0}'.format(config.history_index))


class HistoryClearHandler(webapp2.RequestHandler):
    def get(self):
        """Return all records in the History list"""
        print ('/historyclear')
        self.response.headers['Content-Type'] = 'text/plain'
        config.history_list = []
        config.history_index = -1
        self.response.write(config.history_list)
        self.response.write(' \ncurrent index:{0}'.format(config.history_index))


class NumEqualToHandler(webapp2.RequestHandler):
    def get(self):
        print ('/numequalto?value=val1')
        variable_value = self.request.get('value')
        elements = KeyVal.query().filter(ndb.AND(KeyVal.value == variable_value, KeyVal.enabled == True))
        counter = elements.count()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(counter)#('/numequalto  found this value {0}'.format(counter)+' times')


class EndHandler(webapp2.RequestHandler):
    """Exit the program.
    remove all your data from the application (clean all the Datastore entities).
    Print CLEANED when done."""

    def get(self):
        print ('/end')
        ndb.delete_multi(KeyVal.query().fetch(keys_only=True))
        config.history_list = []
        config.history_index = -1
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('db CLEANED !')


app = webapp2.WSGIApplication([('/', MainHandler), ('/get', GetHandler), ('/set', SetHandler), ('/unset', UnsetHandler), ('/undo', UndoHandler), ('/redo', RedoHandler), ('/historyshow', HistoryShowHandler), ('/historyclear', HistoryClearHandler), ('/numequalto', NumEqualToHandler), ('/end', EndHandler),

                               ], debug=False)
