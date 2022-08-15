from datetime import datetime

from rest_framework.response import Response


def toggle_follow_request(view, request):
    user = request.user
    page = view.get_object()
    if user not in page.followers.all() and user not in page.follow_requests.all():
        follow_request(request.user, view.get_object())
    else:
        unfollow_request(user, page)
    return Response({"status": "follow toggled"})


def follow_request(user, page):
    if page.is_private() == True:
        page.follow_requests.add(user)
    else:
        page.followers.add(user)
    page.save()


def unfollow_request(user, page):
    if user in page.followers.all():
        page.followers.remove(user)
    else:
        page.follow_requests.remove(user)
    page.save()


def toggle_page_is_blocked(view, request):
    page = view.get_object()
    if view.action == "permablock":
        if page.is_permamently_blocked == True:
            return Response({"status": "was already blocked"})
        else:
            page.is_permamently_blocked = True
    elif view.action == "unblock":
        if not page.is_blocked_atm() and page.is_permamently_blocked == False:
            return Response({"status": "was not blocked"})
        else:
            page.is_permamently_blocked = False
            page.unblock_date = datetime.utcnow()
    elif view.action == "timeblock":
        pass
    page.save()
    return Response({"status": "page toggled"})
