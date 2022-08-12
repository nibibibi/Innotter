from rest_framework.response import Response
from users.models import User


def toggle_follow_or_request_invitation(view, request):
    user = request.user
    page = view.get_object()
    is_in_requests = user in page.follow_requests.all()
    is_in_followers = user in page.followers.all()
    if user in page.blacklisted_users.all(): # TODO: replace with permission
        return Response({'status': "user blacklisted"})
    if view.action == 'follow':
        if is_in_followers or is_in_requests:
            return Response({'status': "is already following"})
        elif page.is_private:
            page.follow_requests.add(user)
        else:
            page.followers.add(user)
        page.save()
        return Response({'status': "followed"})
    elif view.action == 'unfollow':
        if is_in_followers:
            page.followers.remove(user)
        elif is_in_requests:
            page.follow_requests.remove(user)
        else:
            return Response({'status': "was not following"})
        page.save()
        return Response({'status': "unfollowed"})
    