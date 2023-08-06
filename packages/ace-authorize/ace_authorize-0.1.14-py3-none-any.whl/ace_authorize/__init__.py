from logging import StreamHandler

import jwt
import requests
from functools import wraps
from firebase_admin import firestore
from flask import request, abort, json, jsonify, make_response
from os import getenv
import logging
import base64

logger = logging.getLogger("ace_authorize")
handler = StreamHandler()
formatter = logging.Formatter('[%(levelname)s] [%(name)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def authorize(scope):
    def decorator(endpoint_func):
        @wraps(endpoint_func)
        def decorated_function(*args, **kwargs):
            tenant_id = kwargs.get('tenant_id')
            host = getenv("ROLES_HOST")

            # if we dont have the roles_host, error out
            if not host:
                return abort(make_response(jsonify({"error": f"authorization host not set"}), 403))

            # API Gateway hides the original token in a custom header (it needs the original Auth header for its internal auth)
            if 'X-Forwarded-Authorization' in request.headers:
                auth_header = request.headers.get('X-Forwarded-Authorization')
            else:
                auth_header = request.headers.get('Authorization')

            encoded_token = auth_header.rpartition(' ')[2]

            # construct data for the request
            body = {
                "scope": scope,
                "resources": kwargs
            }
            if tenant_id is not None:
                body.update({"tenant_id": tenant_id})

            # sent user token as bearer token and body as json body to the ACE authorization endpoint
            # also sent a x-ACE header. We can use that to see if the request is coming from a module during authorization for statistics
            headers = {
                'Authorization': 'Bearer ' + encoded_token,
                'x-ACE': 'module'
                }
            
            url = f"{host}/roles/authorization"
            try:
                response = requests.post(url, json=data, headers=headers)
            except:
                return abort(make_response(jsonify({"error": f"Something went wrong while checking authorization"}), 500))

            # if response is 200
            if response.status_code == 200:
                return endpoint_func(*args, **kwargs)

            # if response is not 200, get the body from the response and return that
            return abort(make_response(response.json, 403))

        return decorated_function
    return decorator
