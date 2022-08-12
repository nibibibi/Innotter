from rest_framework import exceptions
from users.models import User
from rest_framework.response import Response


def toggle_is_blocked(user, action):
    if user.role == User.Roles.ADMIN:
            raise exceptions.PermissionDenied("You have no persmission to perform this action.")
    elif user.is_blocked == True and action == 'block':
        return Response({'status':'was already blocked'})
    elif user.is_blocked == False and action == 'unblock':
        return Response({'status':'was alsready unblocked'})
    
    user.is_blocked = True if action == 'block' else False
    user.save()
        
    return Response({'status': 'toggled'})