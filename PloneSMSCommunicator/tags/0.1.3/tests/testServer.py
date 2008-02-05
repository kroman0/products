import SimpleHTTPServer
import BaseHTTPServer

class SimpleXiamHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200,'OK')
        cl = int(self.headers['content-length'])
        print self.rfile.read(cl)


httpd = BaseHTTPServer.HTTPServer(("", 10010), SimpleXiamHandler)

print 'listen port 10010'
httpd.serve_forever()