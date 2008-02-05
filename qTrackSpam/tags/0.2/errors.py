class TrackbackError(Exception):

    def __init__(self, code, message=None):
        self.code = code
        self.message = message

class BlacklistedURL(Exception):

    def __init__(self, url, match=None):
        self.url = url
        self.match = match

