#!/usr/bin/env python
# -*- coding:utf-8 -*-

#フォト蔵APIのPythonラッパー

import os
import httplib
import base64
import getpass

user_info = None
user_info_file = 'photozou.dat'

def nop():
    header = {'Authorization' : 'Basic %s' % user_info}
    conn = httplib.HTTPConnection('api.photozou.jp')
    conn.request('GET', '/rest/nop/', '', header)
    r1 = conn.getresponse()
    print r1.status, r1.reason
    print r1.read()

def createUserInfo():
    username = raw_input('username > ')
    password = getpass.getpass('password > ')
    encode_str = base64.b64encode('%s:%s' % (username, password))
    return encode_str

def saveUserInfo(user_info):
    f = open(user_info_file, 'w')
    f.write(user_info)
    f.close()
    os.chmod(user_info_file, 0600)
 
def loadUserInfo():
    f = open(user_info_file, 'r')
    txt = f.read()
    f.close()
    return txt

if __name__ == '__main__':
    if os.path.exists(user_info_file):
        user_info = loadUserInfo()
    else:
        user_info = createUserInfo()
        saveUserInfo(user_info)
    nop()
