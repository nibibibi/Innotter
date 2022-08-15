from rest_framework.response import Response


def toggle_block_unblock(view):
    user_to_block = view.get_object()
    if user_to_block.is_blocked == False:
        block_user(user_to_block)
    else:
        unblock_user(user_to_block)
    return Response({'status': "user toggled"})
    
        
def block_user(user):
    user.is_blocked = True
    user.save()
    
def unblock_user(user):
    user.is_blocked = False
    user.save()
    
