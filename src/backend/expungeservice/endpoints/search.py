"""Flask endpoint for searching the remote site. The web app will send `POST`
requests to this endpoint with search parameters in the body of the request.
This endpoint will then send a request to the remote site.

Data format TBD.

Look in slack channel for remote site login

"""

from flask.views import MethodView
from flask.wrappers import Response

from expungeservice.crawler.crawler import Crawler

class SearchQuery(MethodView):
    def __init__(self):
        self.query = None
        self.login_info = None
        self.search_results = None
        self.request = None
        self.crawler = Crawler()
        self.crawler_login = None


    def post(self):
        self.crawler.login('username', 'password')
        record = self.crawler.search('john', 'doe')

        # expunger = Expunger(record)
        # expunged = expunger.run()

        # if expunged:
        if record:
            return Response('success', status=200)
        else:
            return Response('unsuccessful', 404)


def register(app):
    #SearchQuery.crawler_init.methods = ['POST']
    # app.add_url_rules will go here
    app.add_url_rule('/api/v0.1/search', view_func=SearchQuery.as_view('search'))
#    app.add_url_rule('/api/v0.1/search/crawler_init', SearchQuery.crawler_init)


