# python3 -m http.server
# http://localhost:8000/

# python3 http.server documentation:    https://docs.python.org/3/library/http.server.html
# python3 socketserver documentation:   https://docs.python.org/3/library/socketserver.html
# create web server instructions / info:    https://pythonbasics.org/webserver/
# generate index.html file:     https://stackoverflow.com/questions/25024128/python-how-to-programmatically-generate-index-html-file-to-list-contents-of-an


from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, HTTPServer
import http.server, socketserver
import time, os

#####
HOST = "localhost"       # host name
PORT = 8000              # port 8000: used for development, shouldn't be directly exposed to internet

HTML_FILE = "/home/fiona/projects/fi_src/python/dts/index.html"

#####


### create web server
class MyHttpRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = 'index.html'
        return SimpleHTTPRequestHandler.do_GET(self)


def dts_webserver():
    Handler = MyHttpRequestHandler
 
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Http Server Serving at port", PORT)
        httpd.serve_forever()

dts_webserver()

