#!/usr/bin/env python
# -*- coding:utf-8 -*-

#フォト蔵APIのPythonラッパー

import os
import httplib
import base64
import getpass
import mimetypes

user_info = None
user_info_file = 'photozou.dat'
boundary = '-----photozou.py-----'

def photo_add(file_name
        , album_id
        , photo_title = ''
        , description = ''
        , tag = ''
        , comment = ''
        , data_type = 'exif'
        , year = ''
        , month = ''
        , day = ''):
    disposition = 'Content-Disposition: form-data; name="%s"'
    values = open(file_name, 'rb').read()
    data = {}
    data['album_id'] = album_id
    data['photo_title'] = photo_title
    data['description'] = description
    data['tag'] = tag
    data['comment'] = comment
    data['data_type'] = data_type
    data['year'] = year
    data['month'] = month
    data['day'] = day
    lines = []
    lines.append('--' + boundary)
    lines.append(disposition % 'photo' + '; filename="%s"' % file_name)
    lines.append('Content-Type: %s' % mimetypes.guess_type(file_name)[0])
    lines.append('')
    lines.append(values)
    for k, v in data.iteritems():
        lines.append('--' + boundary)
        lines.append(disposition % k)
        lines.append('')
        lines.append(v)
    lines.append('--' + boundary + '--')
    lines.append('')
    data_str = '\r\n'.join(lines)

    header = {'Authorization' : 'Basic %s' % user_info}
    header['Content-Type'] = 'multipart/form-data; boundary=%s' % boundary
    conn = httplib.HTTPConnection('api.photozou.jp')
    conn.request('POST', '/rest/photo_add/', data_str, header)
    r1 = conn.getresponse()
    print r1.status, r1.reason
    print r1.read()

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
