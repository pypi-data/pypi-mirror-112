import wikipedia
import requests
import json
import re


def getflagpage(term):
    """Returns the wikipedia page corresponding to the flag associated with the search term, along 
    with a list of alternatives. 

    :param term: A place, person, organisation, etc.
    :type term: String
    
    :return: A list containing the title of the wikipedia page corresponding to the suggested flag,
        and a list of titles for suggested alternative pages
    :rtype: [String, [String]]
    """
    result = None
    searchresults = filterresults(wikipedia.search(f"Flag of {term}"))
    if pageexists(f"Flag of {term}"):
        #TODO Bloody redirects w()
        result = getredirect(f"Flag of {term}")
        altresults = searchresults
    else:
        result = selectflagpage(term, searchresults)
        altresults = searchresults
        return [result, altresults]
    if isdisambiguation(result):
        altresults = getdisambiguationlinks(result)
        result = altresults[0]
    return [result, altresults]

#TODO Make this shit better, cos it sucks right now
def selectflagpage(place, results):
    """Given a list of wikipedia page names, selects one with 'flag' or 'coat of arms' in the
    title and returns it

    :param place: The place who's flag is being searched for
    :type plae: String

    :param results: A list of search results
    :type results: [String]

    :return: The selected result
    :rtype: String
    """
    for result in results:
        if "flag" in result.lower():
            return result
    for result in results:
        if "coat of arms" in result.lower():
            return result

def filterresults(searchresults):
    """Given a list of search results, select all those likely to be for flags or coats of arms
    
    :param searchresults: A list of Strings represnting individual search results
    :type searchresults: [String]
    
    :returns: A list of those results that contained the substrings 'flag' or 'coat of arms' (case
        insensitive)
    :rtype: [String]"""
    return [x for x in searchresults if re.search('flag|coat of arms', x, re.IGNORECASE)]

# Credit goes to DmytroSytro on StackExchange if this works
def getflagurl(pagename):
    """Given the name of a wikipedia page, returns a representitive image for that page. It can be 
    safely assumed that, if the wikipedia page corresponds to a flag, the representitive image will
    be that flag
    
    :param pagename: The name of a wikipedia page
    :type pagename: String
    
    :return: The url of the representitive image for the page with name pagename
    :rtype: String"""
    WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&pilicense=any&piprop=original&titles='
    response  = requests.get(WIKI_REQUEST+pagename)
    json_data = json.loads(response.text)
    img_link = list(json_data['query']['pages'].values())[0]['original']['source']
    return img_link

#Checks if a wikipedia page exists
#   Note: case sensitive
def pageexists(pagename):
    """Given a page name, returns True if there is a page on wikipedia with that name.

    :param pagename: The name of a wikipedia page
    :type pagename: String
    
    :return: True if pagename is the name of a wikipedia page, False otherwise
    :rtype: Boolean
    """
    url = constructpageurl(pagename)
    if requests.get(url).status_code == 200:
        return True
    else: 
        return False

# Makes a url to a wikipedia page based on plaintext pagename
def constructpageurl(pagename):
    """Given a natural-text page name, e.g 'Flag of Thailand', returns a url pointing to a wikipedia
    page (if one exists) for that page name
    
    :param pagename: The name of a wikipedia page
    :type pagename: String
    
    :return: The url of a wikipedia page with the name pagename
    :rtype: String"""
    pagenamehyphen = pagename.replace(' ', '_')
    url = "https://en.wikipedia.org/wiki/" + pagenamehyphen
    return url

def getredirect(pagename):
    """Given a wikipedia page name, if the page name refers to a redirect, returns the name of the 
    page that the redirect points to; Otherwise, returns the input

    :param pagename: The name of a wikipedia page
    :type pagename: String
    
    :return: The absolute name of the page pointed to by pagename
    :rtype: String
    """
    pagenamehyphen = pagename.replace(' ', '_')
    query = requests.get(f'https://en.wikipedia.org/w/api.php?action=query&titles={pagenamehyphen}&&redirects&format=json')
    data = json.loads(query.text)
    if 'redirects' in data['query']:
        return data['query']['redirects'][0]['to']
    else:
        return pagename

def isdisambiguation(pagename):
    """Given a wikipedia page name, returns True if that page is a disambiguation page and False otherwise
    
    :param pagename: The name of a wikipedia page
    :type pagename: String
    
    :return: True if pagename is the name of a wikipedia page in the 'All disambiguation pages' 
        category, otherwise False
    :rtype: Boolean
    """
    pagenamehyphen = pagename.replace(' ', '_')
    query = requests.get(f'https://en.wikipedia.org/w/api.php?action=query&format=json&titles={pagenamehyphen}&prop=categories')
    data = json.loads(query.text)
    for category in data['query']['pages'][next(iter(data['query']['pages'].keys()))]['categories']:
        catname = category['title']
        if catname == "Category:All disambiguation pages":
            return True
    return False

def getdisambiguationlinks(pagename):
    """Given a wikipedia page name corresponding to a disambiguation page, returns all of the pages
    it branches to.
    
    :param pagename: The name of a wikipedia page
    :type pagename: String
    
    :return: A list of page names, corresponding to every page that the disambiguation suggests as
        corresponding to the pagename
    :rtype: [String]
    """
    links = []
    pagenamehyphen = pagename.replace(' ', '_')
    query = requests.get(f'https://en.wikipedia.org/w/api.php?action=query&format=json&titles={pagenamehyphen}&prop=links')
    data = json.loads(query.text)
    for link in data['query']['pages'][next(iter(data['query']['pages'].keys()))]['links']:
        if not link['title'] in [f'Talk:{pagename}', 'Help:Disambiguation']:
            links.append(getredirect(link['title']))
    return links
