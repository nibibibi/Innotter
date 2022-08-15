from rest_framework import exceptions
from users.models import User
from rest_framework.response import Response


def toggle_is_blocked(user, action):
    if user.is_blocked and action == 'block':
        return Response({'status':'was already blocked'})
    elif (not user.is_blocked) and (action == 'unblock'):
        return Response({'status':'was already unblocked'})
    
    user.is_blocked = True if action == 'block' else False
    user.save()
        
    return Response({'status': 'user toggled'})