from datetime import datetime, timedelta
from os import access
import jwt
from django.conf import settings

def generate_access_token(user):
    
    access_token_payload = {
        'user_id': user.id,
        'expires_at': datetime.utcnow() + timedelta(days=0, minutes=5),
        'created_at': datetime.utcnow()
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    
    return access_token

def generate_refresh_token(user):
    
    refresh_token_payload = {
        'user_id': user.id,
        'expires_at': datetime.utcnow() + timedelta(days=1),
        'created_at': datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')
    
    return refresh_token