from flask_restful import Resource, reqparse
from flask import request, jsonify
from v1_0.common.auth import Auth
#Request POST arguments 
parser = reqparse.RequestParser()

class AuthSrc(Resource):
    def post(self):
        if request.path == '/auth/google':
            parser.add_argument(
                'username',
                required=True,
                help="username cannot be blank"
            )
            print 'google'
            auth = Auth()
            token = auth.loginGoogle(request.json)
            return jsonify(token=token)
        elif request.path == '/auth/facebook':
            print 'facebook'
            auth = Auth()
            token = auth.loginFacebook(request.json)
            return jsonify(token=token)
        elif request.path == '/auth/live':
            print 'live'
            print request.json
        elif request.path == '/auth/self':
            print 'self'
            auth = Auth()
            token = auth.loginSelf(request.json)
            return jsonify(token=token)