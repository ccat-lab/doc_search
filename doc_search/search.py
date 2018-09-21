# -*- coding: utf-8 -*-

import http.client, urllib.parse, json

# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = "subscriptionKey"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing Web search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/search"

class BingWebSearchResult:
    "Class for holding a single Bing Web Search Result"
    
    def __init__(self, result, rank):
        self.rank = rank
        self.raw_result = result
        self.url = result.get('url')
        self.name = result.get('name')
        self.snippet = result.get('snippet')

class BingWebSearchResponse:
    "Class for holding and managing Bing Search Responses"
    
    def __init__(self, response):
        self.headers = response.getheaders()
        self.body = response.read().decode('utf-8')
        self.response_json = json.loads(self.body)
        self.search_query = self.response_json.get('queryContext').get('originalQuery')

        # Package up the search results 
        if 'webPages' in self.response_json:
            self.results = []
            for rank, result in enumerate(self.response_json['webPages']['value']):
                self.results.append(BingWebSearchResult(result, rank))

        else:
            self.results = None
     

def BingWebSearch(searchterm,
                  count = 5,
                  responseFilter = 'Webpages',
                  advancedOperators = None):
    "Performs a Bing Web search and returns the results."

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    if advancedOperators:
        searchterm = searchterm +" " + " ".join(["{}:{}".format(k,v) 
                                      for k,v in advancedOperators.items()])
    query = urllib.parse.quote(searchterm)
    conn.request("GET", path + "?q=" + query + "&count={}".format(count), 
                                                           headers=headers)
    resp = conn.getresponse()
    response = BingWebSearchResponse(resp)
    headers = [k + ": " + v for (k, v) in resp.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]

    return response
    

if __name__ == "__main__":
    r = BingWebSearch('elephants', advancedOperators = {'site':'en.wikipedia.org'})
    if r.results:
        print(r.search_query)
        for i in r.results:
            print(i.name)
            print(i.url)
    else:
        print('No response?')
        print(r.body)

