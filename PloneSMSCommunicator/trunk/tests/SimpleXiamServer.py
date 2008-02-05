import SimpleHTTPServer

class SimpleXiamHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def assertEqual(self, first, second):
        try:
            assert(first == second)
        except:
            raise AssertionError, '%s != %s' % (first, second)

    def send_response(self):
        self.send_header('', self.version_string())

    def do_POST(self):
        self.send_response()
