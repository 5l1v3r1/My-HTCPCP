#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
from Crypto.Cipher import AES
import base64
import random
import time
from urllib.parse import urlparse, parse_qs
import json

def reverse(s):
    return ''.join(reversed(s))

def get_key(x_sign):
    i = [ c for c in hashlib.md5(reverse(x_sign).encode()).hexdigest()[8: 24].upper() ]
    for a in range(0, int(len(i) / 2)):
        o = i[2 * a]
        i[2 * a] = i[2 * a + 1]
        i[2 * a + 1] = o
    return "".join(i)

pad_pkcs5 = lambda x, y: x + (y - len(x) % y) * chr(y - len(x) % y).encode("utf-8")
unpad_pkcs5 = lambda x: x[:-int(x[-1])]

def decrypt(en_data, key):
    password = key.encode("utf-8")
    iv = reverse(key).encode("utf-8")
    cipher = AES.new(password, AES.MODE_CBC, iv)
    data = unpad_pkcs5(cipher.decrypt(base64.b64decode(en_data)))
    return data

def get_nonce():
    A = [0]*36
    d = "0123456789abcdef"
    for i in range(0, 36):
        A[i] = d[random.randint(0, 15)]
    A[14] = "4"
    A[19] = d[3 & ord(A[19]) | 8]
    A[8] = A[13] = A[18] = A[23] = "-"
    return "".join(A)

def get_timestamp():
    return str(int(time.time() * 1000))

def ser_data(url, method, content_type="application/json", data={}):
    s_data = {}
    qs = parse_qs(urlparse(url).query)
    for i in qs:
        v = qs[i][0] if qs[i] else ""
        s_data[i] = v
    method = method.lower()
    post_data = ""
    if method!="post":
        return s_data, post_data
    if content_type=="application/x-www-form-urlencoded" or content_type=="application/octet-stream" \
        or content_type.startswith("multipart/form-data"):
        s_data.update(data)
    else:
        post_data = json.dumps(data)
    return s_data, post_data

def hex_encode(s):
    data = "\\u".join("{:04X}".format(ord(c)) for c in s)
    if data:
        data = "\\u"+data
    return data

def get_sign(s_data, post_data, nonce, timestamp):
    sorted_data = []
    for key in sorted(s_data):
        if s_data[key]:
            sorted_data.append(f"{hex_encode(key)}={hex_encode(s_data[key])}")
    if post_data:
        sorted_data.append(hex_encode(post_data))
    sorted_data.append(f"nonce={nonce}")
    sorted_data.append(f"timestamp={timestamp}")
    joined_data = "&".join(sorted_data)
    tmp1_md5 = hashlib.md5(f"{nonce}@@{timestamp}".encode()).hexdigest()
    tmp2_md5 = hashlib.md5(base64.b64encode(joined_data.encode())).hexdigest()
    return hashlib.md5(f"[{tmp1_md5}#{tmp2_md5}#{tmp1_md5}]".encode()).hexdigest()

if __name__ == '__main__':
    x_sign = "a7c0d5c26f4ff0656cd4b6c11e8c9c19"
    en_data = "b64 en data"
    print(decrypt(en_data, get_key(x_sign)))