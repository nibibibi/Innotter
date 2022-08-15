from datetime import datetime

from rest_framework.response import Response

from ..models import Page


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

def toggle_page_permamently_blocked(view, request): # Request may be needed later in case we want to know who blocked the page
    page = view.get_object()
    if page.is_permamently_blocked == True:
        print("unpermablocking...")
        unpermablock_page(page=page)
    else:
        print("permablocking...")
        permablock_page(page=page)
    return Response({'status': "page state toggled"})

def permablock_page(page: Page):
    page.is_permamently_blocked = True
    page.save()
    
def unpermablock_page(page: Page):
    page.is_permamently_blocked = False
    page.save()
