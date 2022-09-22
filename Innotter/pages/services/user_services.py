from rest_framework.response import Response


def toggle_block_unblock(view):
    user_to_block = view.get_object()
    message = block_user(user_to_block) if not user_to_block.is_blocked else unblock_user(user_to_block)
    return message


def block_user(user):
    user.is_blocked = True
    user.save()
    return {'status': "user blocked"}


def unblock_user(user):
    user.is_blocked = False
    user.save()
    return {'status': "user unblocked"}
