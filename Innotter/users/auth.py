import datetime
from django.conf import settings

import jwt


def generate_access_token(user):

    access_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(
            hours=1
        ),  # TODO: change "exp" to 5 min (1 hour set up for testing)
        "iat": datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )

    return access_token


def generate_refresh_token(user):

    refresh_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )

    return refresh_token
