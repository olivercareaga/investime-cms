# -*- coding: utf-8 -*-

'''
Created on 19 de oct. de 2015

@author: Oliver Careaga
'''
from cgi import parse_qs
from sys import path as syspath
from os import path as ospath

'''
Functions and properties of 'os.path'

os.path.abspath | Return absolute path with backslashes
os.path.join | Join paths separated by comma
os.path.dirname() | Return file's directory
'''
syspath.append(ospath.abspath(ospath.join(ospath.dirname(__file__), 'modules')))

from multilingual import Multilingual


def application(environ, start_response):

    start_response('200 OK', [('Content-Type', 'application/json')])

    requestBody = environ['wsgi.input'].read()
    parsedBody = parse_qs(str(requestBody)[2:-1])

    ml = Multilingual(parsedBody.get('database')[0])
    pageObject = ml.getPageObject(parsedBody.get('pageCode')[0], parsedBody.get('languageCode')[0])

    return [pageObject.encode('utf-8')]

    '''
    Try returns

    return [parsedBody.get('database', 'X')[0].encode('utf-8')]

    Environ values

    serverName = environ['SERVER_NAME']
    scriptName = environ['SCRIPT_NAME']
    pathName = environ['REQUEST_URI']
    '''
