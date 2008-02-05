import md5

def encrypt(s):
    return md5.new(s).hexdigest().upper()