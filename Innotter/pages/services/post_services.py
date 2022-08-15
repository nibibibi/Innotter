from rest_framework.response import Response


def toggle_is_favourite(view, request):
    post = view.get_object()
    user = request.user
    if view.action == 'favoutire':
        if post in user.favourite_posts.all():
            return Response({'status': "already in favourites"})
        else:
            user.favourite_posts.add(post)
    if view.action == 'unfavourite':
        if post not in user.favourite_posts.all():
            return Response({'status': "was not in favourites"})
        else:
            user.favourite_posts.remove(post)
    user.save()
    return Response({'status': "favourites edited"})