#! /usr/bin/env python
class Tag(object):
    """ Produces HTML in fly"""
    def __init__(self, css = None, js = None):
        if css == None:
            self.__css = "bootstrap.css"
        else:
            self.__css = css
        if js == None:

            self.__js = ["https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"]\
            #List of required JS files.
            self.__js.append("http://autobahn.tablesorter.com/jquery.tablesorter.min.js")
            self.__js.append("jquery.tablesorter.pager.js")
            self.__js.append("tablesorterscript.js")
        else:
            self.__js = js

        self.__content = []
        self.create_tag = ""
        self.keys = []
        self.innerHTML = ""
        self.close_tag = ""



    def create_js(self):
        """To create JS files"""
        for x in self.__js:
            self.__content.append("<script src=\"%s\"></script>\n"% (x))


    def create_css(self):
        self.__content.append("<link href = \"%s\" rel = \"stylesheet\">"% \
                                                             (self.__css))
    def create_value(self, name, values):
        """create HTML tag value"""
        self.innerHTML = values
        self.__content.append(self.innerHTML)
    
    def end_tag(self, name):
        self.close_tag = "\n</%s>\n" %(name)
        self.__content.append(self.close_tag)
        if name == "body":
            self.end_tag("html")


    def create_normal(self, name, attributes = None, values = None):
        #create a tag 
        self.create_tag = "<%s"% (name)
        if attributes != None:
            self.keys = attributes.keys()
            for x in self.keys:
                self.create_tag +=" %s=\"%s\""% (x, attributes[x])
        self.create_tag += ">\n"
        self.__content.append(self.create_tag)
        if values != None:
            self.create_value(name, values)
           

    def create_table(self, name, attributes, headers, values):
        #create a HTML Table
        self.create_normal(name, attributes)
        self.create_normal(name = "tr")
        for x in headers:
            self.create_normal(name = "th", attributes = {'class' : \
                                 'yellow header headerSortDown'}, values = x)
            self.end_tag("th")
        self.end_tag("tr")

        for x in values:
            self.create_normal(name = "tr")
            self.create_normal(name = "td", values = str(x['id']))
            self.end_tag("td")
            self.create_normal(name = "td", values = str(x['ups']))
            self.end_tag("td")
            self.end_tag("tr")
        self.end_tag(name)


    def body_tag(self, attributes = None):
        self.end_tag("head")
        self.create_normal("body", attributes)
       
    def print_to_file(self):
        self.file_name = "reddit-comment.html"
        with open(self.file_name, "w") as f:
            for x in self.__content:
                f.write(x)


        

