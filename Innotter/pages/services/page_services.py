from rest_framework.response import Response

from users.models import User

from ..models import Page, Tag


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


def toggle_page_permamently_blocked(
    view, request
):  # Request may be needed later in case we want to know who blocked the page
    page = view.get_object()
    if page.is_permamently_blocked == True:
        print("unpermablocking...")
        unpermablock_page(page=page)
    else:
        print("permablocking...")
        permablock_page(page=page)
    return Response({"status": "page state toggled"})


def permablock_page(page: Page):
    page.is_permamently_blocked = True
    page.save()


def unpermablock_page(page: Page):
    page.is_permamently_blocked = False
    page.save()


def accept_follow_request(view, request, pk=None):
    page = view.get_object()
    user = page.follow_requests.all().filter(pk=request.data.get("user_id")).first()
    if user is None:
        return Response({"status": "no user in follow_requests"})
    else:
        page.followers.add(user)
        page.follow_requests.remove(user)
        page.save()
        return Response({"status": "user moved"})


def reject_follow_request(view, request):
    page = view.get_object()
    user = page.follow_requests.all().filter(pk=request.data.get("user_id")).first()
    if user is None:
        return Response({"status": "no user in follow_requests"})
    else:
        page.follow_requests.remove(user)
        page.save()
        return Response({"status": "request rejected"})


def reject_all_follow_requests(view, request):
    page = view.get_object()
    page.follow_requests = []
    page.save()
    return Response({"status": "follow_requests cleared"})


def toggle_page_is_private(view, request):
    page = view.get_object()
    if page.is_private == False:
        page.is_private = True
    else:
        page.is_private = False
    page.save()
    return Response({"status": "page privacy toggled"})


def toggle_page_tag(view, request):
    page = view.get_object()
    tag = Tag.objects.filter(name=request.data.get("tag_name")).first()
    if tag is None:
        return Response({"status": "tag does not exist yet"})
    elif tag in page.tags.all():
        page.tags.remove(tag)
    else:
        page.tags.add(tag)
    page.save()
    return Response({"status": "tag toggled"})
