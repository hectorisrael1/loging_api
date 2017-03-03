#!/usr/bin/python
'''
Created on 03 de marzo de 2017

@author: hgonzalez(Hector Gonzalez)
'''
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from v1_0.common.cache import cache

from v1_0.resources.authSrc import AuthSrc

app = Flask(__name__)
cache.init_app(app, config={
                            'CACHE_TYPE':'memcached',
                            'CACHE_KEY_PREFIX':'cache_',
    	                    #'CACHE_MEMCACHED_SERVERS':['172.16.1.112'],
                            #'CACHE_MEMCACHED_USERNAME':None,
                            #'CACHE_MEMCACHED_PASSWORD':None
                            })
"""configuration headers"""
CORS(app)

""" Instance Flask Restful """
api = Api(app)

api.add_resource(AuthSrc, '/auth/facebook', '/auth/live','/auth/google','/auth/self')

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')