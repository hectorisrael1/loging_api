import logging
import requests
from datetime import datetime, timedelta
import jwt
import simplejson as json
from cache import cache

logging.basicConfig()
log = logging.getLogger("auth_logger")
log.setLevel(logging.DEBUG)

class Auth():
    FACEBOOK_SECRET = '574a96ae8cd34219d9df255edd3e473d'
    GOOGLE_SECRET = 'ExIhKZefcYA54OUwhfub8PEH'
    LIVE_SECRET = 'WX89DoeM46k1fb4nNxSwboR'
    TOKEN_SECRET = '063b408378198cfe9b72f7f7ed2ff2836c47286df83aae98'
    def __init__(self):
        pass
    def create_token(self,user):
        payload = {
            'sub': user,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        token = jwt.encode(payload, self.TOKEN_SECRET)
        token = token.decode('unicode_escape')
        print 'token creado '
        print token
        cache.set('token_'+token, user, 86400)
        print ' '
        print 'token cacheado'
        print cache.get('token_'+token) 
        return token
    
    def parse_token(self,req):
        token = req.headers.get('Authorization').split()[1]
        return jwt.decode(token, self.TOKEN_SECRET)
    
    def loginFacebook(self,params):
        access_token_url = 'https://graph.facebook.com/v2.7/oauth/access_token'
        graph_api_url = 'https://graph.facebook.com/v2.7/me'
        params = {
            'client_id': params['clientId'],
            'redirect_uri': params['redirectUri'],
            'client_secret': self.FACEBOOK_SECRET,
            'code': params['code']
        }
        # Step 1. Exchange authorization code for access token.
        r = requests.get(access_token_url, params=params)
        access_token = { 'access_token':r.json()['access_token']}
    
        # Step 2. Retrieve information about the current user.
        r = requests.get(graph_api_url, params=access_token)
        profile = json.loads(r.text)
        print profile['id']
        token = self.create_token(profile['id'])
        return token
        
    def loginLive(self):
        return 'loginLive'
    
    
    def loginGoogle(self,params):
        access_token_url = 'https://accounts.google.com/o/oauth2/token'
        people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'
    
        payload = dict(client_id=params['clientId'],
                       redirect_uri=params['redirectUri'],
                       client_secret=self.GOOGLE_SECRET,
                       code=params['code'],
                       grant_type='authorization_code')
        # Step 1. Exchange authorization code for access token.
        r = requests.post(access_token_url, data=payload)
        token = json.loads(r.text)
        headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}
        # Step 2. Retrieve information about the current user.
        r = requests.get(people_api_url, headers=headers)
        profile = json.loads(r.text)
        print profile['sub']
        
        return self.create_token(profile['sub'])
    
    def loginSelf(self,params):
        token = self.create_token(params['email'])
        print 'token retornado'
        print token
        return token