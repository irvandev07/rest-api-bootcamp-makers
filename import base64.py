import base64
from email.mime import base

from itsdangerous import base64_encode


def car_manufaktur():
    b = 'dXNlcm5hbWU6cGFzc3dvcmQ='
    c = base64.b64decode(b)
    e = c.decode("ascii")
    # base64_bytes = base64.encode("ascii")
    # str_bytes = base64.b64decode(base64_bytes)
    # a = 'eW91ciB0ZXh0'
    # base64.b64decode(a)
    # userAndPass = base64.b64encode(b"username:password").decode("ascii")
    # endoce_ = base64.encode('ascii')
    # header = { 'Authorization' : 'Basic %s' %  b64Val }
    return e
print(car_manufaktur())