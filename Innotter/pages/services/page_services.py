from ..models import Page, Tag


def toggle_follow_request(view, request):
    user = request.user
    page = view.get_object()
    if user not in page.followers.all() and user not in page.follow_requests.all():
        message = follow_request(request.user, view.get_object())
    else:
        message = unfollow_request(user, page)
    return message


def follow_request(user, page):
    if page.is_private() is True:
        page.follow_requests.add(user)
    else:
        page.followers.add(user)
    page.save()
    return {'status': "page followed"}


def unfollow_request(user, page):
    if user in page.followers.all():
        page.followers.remove(user)
    else:
        page.follow_requests.remove(user)
    page.save()
    return {'status': "page unfollowed"}


def toggle_page_permamently_blocked(view, request):
    page = view.get_object()
    if page.is_permamently_blocked:
        message = unpermablock_page(page=page)
    else:
        message = permablock_page(page=page)
    return message


def permablock_page(page: Page):
    page.is_permamently_blocked = True
    page.save()
    return {'status': "page blocked"}


def unpermablock_page(page: Page):
    page.is_permamently_blocked = False
    page.save()
    return {'status': "page unblocked"}


def accept_follow_request(view, request, pk=None):
    page = view.get_object()
    user = page.follow_requests.all().filter(pk=request.data.get("user_id")).first()
    if user is None:
        return {'status': "user not found"}
    else:
        page.followers.add(user)
        page.follow_requests.remove(user)
        page.save()
        return {'status': "request accepted"}


def reject_follow_request(view, request):
    page = view.get_object()
    user = page.follow_requests.all().filter(pk=request.data.get("user_id")).first()
    if user is None:
        return {'status': "user no found"}
    else:
        page.follow_requests.remove(user)
        page.save()
        return {'status': "request rejected"}


def reject_all_follow_requests(view, request):
    page = view.get_object()
    page.follow_requests = []
    page.save()
    return {'status': "requests rejected"}


def toggle_page_is_private(view, request):
    page = view.get_object()
    if not page.is_private:
        page.is_private = True
        message = {'status': "switched to private"}
    else:
        page.is_private = False
        message = {'status': "switched to public"}
    page.save()
    return message


def toggle_page_tag(view, request):
    page = view.get_object()
    tag = Tag.objects.filter(name=request.data.get("tag_name")).first()
    if tag is None:
        return {'status': "tag not found"}
    elif tag in page.tags.all():
        page.tags.remove(tag)
    else:
        page.tags.add(tag)
    page.save()
    return {'status': "tag toggled"}
