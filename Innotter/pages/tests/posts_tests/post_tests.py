import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from users.auth import generate_access_token
from users.models import User

from pages.models import Post
from pages.serializers.post_serializers import PostSerializer
from pages.tests.pages_tests.conftest import page
from pages.tests.posts_tests.conftest import post, posts
from pages.tests.users_tests.conftest import user
from pages.views.post_views import PostViewSet

pytestmark = pytest.mark.django_db

default_viewset = PostViewSet.as_view(
    {"get": "retrieve", "post": "create", "delete": "destroy"}
)
list_viewset = PostViewSet.as_view({"get": "list"})
toggle_favourite_viewset = PostViewSet.as_view({"post": "favourite"})


class TestPostLogic:
    def test_create_post(self, user: user, api_factory: APIRequestFactory, page: page):
        page.owner = user
        page.save()
        request_data = {"page": page.pk, "content": "somecontent", "reply_to": ""}
        request = api_factory.post(reverse("posts-detail", args=[1]), request_data)
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = default_viewset(request)

        assert (
            response.status_code == 201
            and response.data == PostSerializer(Post.objects.first()).data
        )

    def test_destroy_post(self, user: user, post: post, api_factory: APIRequestFactory):
        assert len(Post.objects.all()) == 1 and Post.objects.first() == post
        post.page.owner = user
        post.page.save()
        request = api_factory.delete(reverse("posts-detail", args=[post.pk]))
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = default_viewset(request, pk=post.pk)

        assert response.status_code == 204 and len(Post.objects.all()) == 0

    def test_retrieve_post(
        self, user: user, post: post, api_factory: APIRequestFactory
    ):
        request = api_factory.get(reverse("posts-detail", args=[post.pk]))
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = default_viewset(request, pk=post.pk)

        assert (
            response.status_code == 200 and response.data == PostSerializer(post).data
        )

    def test_list_posts(self, user: user, posts: posts, api_factory: APIRequestFactory):
        request = api_factory.get(reverse("posts-list"))
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = list_viewset(request)

        assert response.status_code == 200 and len(response.data) == len(posts)
        assert response.data == PostSerializer(posts, many=True).data

    def test_toggle_post_favourite(
        self, post: post, user: user, api_factory: APIRequestFactory
    ):
        assert len(user.favourite_posts.all()) == 0
        request = api_factory.post(reverse("posts-favourite", args=[post.pk]))
        token = generate_access_token(user)
        force_authenticate(request=request, user=user, token=token)
        response = toggle_favourite_viewset(request, pk=post.pk)
        user = User.objects.get(pk=user.pk)
        assert response.status_code == 200 and response.data.get("status") == "toggled"
        assert (
            len(user.favourite_posts.all()) == 1
            and user.favourite_posts.first() == post
        )
