#! /usr/bin/env python
from urllib2 import urlopen
from simplejson import loads
from sys import argv, exit
from urlparse import urlparse
from HTMLparser import Tag
import webbrowser

"""
   This is main file which import HTMLparser which will generate html on fly.
   We need urlopen to read the contents of the json file and it is imported \
   from urllib2 module.
   Need json module to parse the received URL, simplejson module has loads \
   which will convert json to python list data type.
   urlparse is quite new addition to python since 2.5 and mentioned in RFC 1808.
   argv is imported from sys module to get url from command line, exit to quit
   the application in case of any error.
   open_new_tab is needed to open html file created by the program automatically
"""


def sample():
    """ Prints the sample compilation process."""
    return "Sample:$python redditbot.py http://www.reddit.com/r/programming/\
           comments/ioor4/reviews_the_book_of_weird_ruby"

def check_url(url = None):
    """ To check passed URL is valid reddit url """
    if url is None or url is " ":
        print ("URL is empty")
        print sample()
        exit()
    else:
        """Will append http if url startswith www and then parses """
        url = url.lower()
        if url.startswith('www'):
            url = "http://%s"%(url)
        parsed_url = urlparse(url)
        if parsed_url.scheme == "http" and parsed_url.netloc == \
        'www.reddit.com' and parsed_url.path.startswith(\
        '/r/programming/comments/'):
            if len(parsed_url.path.split('/')) == 6:
                url = url + "/.json"
            elif len(parsed_url.path.split('/')) == 7 and \
                              parsed_url.path.endswith('/'):
                url = url + ".json"
            return url
        else:
            print ("Invalid URL :%s"%(url))
            print sample()
            exit()

def traverse(nested_data):
    for index, item in enumerate(nested_data):
         i_real_data = nested_data[index]['data']
         results.append({'id' : i_real_data['id'], 'ups' : i_real_data\
                                                                    ['ups']})
         if len(i_real_data['replies']) > 0:
             traverse(i_real_data['replies']['data']['children'])

if __name__ == "__main__":
    try:
        if len(argv) is 2:
            results = []#holds final comments and ups
            url = check_url(argv[1])  
            try:
               urlread = urlopen(url).read()
               contents = loads(urlread)
            except ValueError:
               print("Please connect to internet and try again")
               exit()

            starting_point = contents[1]['data']['children']
            for index, item in enumerate(starting_point):
                real_data = starting_point[index]['data']
                results.append({'id' : real_data['id'], 'ups' : \
                                                              real_data['ups']})
                length = len(real_data['replies'])
                if length == 1 :
                    temp = real_data['replies']['data']['children'][0]['data']
                    result.append({'id' : temp['id'], 'ups' : temp['ups'] })
                elif length > 1:
                    traverse(real_data['replies']['data']['children'])
        else:
            print sample()
            exit()
    except Exception as inst:
        # print exception and quit if something goes wrongs while fetching the \
        # data
        print inst.message
        exit()

    try:
        # HTML is created on the fly
        html = Tag()
        html.create_normal("html")
        html.create_normal("head")
        html.create_js()
        html.create_css()
        html.body_tag()
        html.create_normal("h3", values = "Comments and Ups for %s"%(argv[1]))
        html.create_table(name = "table", attributes = {'class' : \
                             'zebra-striped', 'id' : 'reddit'},\
                             values = results, headers = ['id', 'ups'])
        html.end_tag("body")
        html.print_to_file()
        browser = webbrowser.get()
        browser.open('reddit-comment.html')

    except Exception as inst:
        print inst.message
           
