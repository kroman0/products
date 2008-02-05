import re

def isUrl(url):
    return re.match(r'(ht|f)tps?://[^\s\r\n]+', url)

def getHostName(server_url):
    host_name = re.search(r'(?<=://)[a-zA-Z0-9.]+', server_url)
    host_name = host_name.group(0)
    return host_name