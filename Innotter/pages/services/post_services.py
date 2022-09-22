def toggle_is_favourite(view, request):
    post = view.get_object()
    user = request.user
    user.favourite_posts.remove(post) if post in user.favourite_posts.all() else user.favourite_posts.add(post)
    user.save()
    return {'status': "toggled"}
