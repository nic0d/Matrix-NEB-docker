from neb.plugins import Plugin

import json
import urllib
import requests
import os

class TAIBot(Plugin):
    """Do a I am Lucky query.
    tai lucky <text>: Do a I am Lucky query
    tai graph <text>: Do a Google Knowledge Graph request.
    """

    name="tai"

    def cmd_lucky(self, event, *args):
        """Do an "I am Lucky query". '!tai lucky <text>'"""
        
        searched_word = event["content"]["body"][11:]
         
        print searched_word
        requested = "http://www.google.com/search?q=" + searched_word + "&btnI=I'm\%20feeling\%20lucky"
# "http://www.google.com/search?q=%s&btnI=I'm%20feeling%20lucky"
        r = requests.get(requested)
        result = r.history[-1].url
        print result
        return result  

    def cmd_graph(self, event, *args):
        """Do a Google Knowledge Graph search. '!tai graph <text>"""
        
        query = event["content"]["body"][11:]
        print "User requested Knowledge Graph search for term: " + query
 
        api_key = os.environ['GOOGLE_API_KEY']

        service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
        params = {
            'query': query,
            'limit': 1,
            'indent': True,
            'key': api_key,
        }
        url = service_url + '?' + urllib.urlencode(params)
        print "Performing query using URL: " + url
        response = json.loads(urllib.urlopen(url).read())
        print response
        try:
            result = response['itemListElement'][0]['result']['detailedDescription']['articleBody']
            result += "\nSource: " + response['itemListElement'][0]['result']['detailedDescription']['url']
            print "Sending the following answer to user:\n" + result
            return result
        except Exception:
            print "Exception while processing query"
            return "Sorry, I couldn't find anything."

