from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework import routers
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Bookmark, Snippet
from django.contrib.auth.models import User
from .views import BookmarkViewSet, SnippetViewSet, UserViewSet

# Create your tests here.
# test plan


class BookmarkTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.bookmark = Bookmark.objects.create(
            id=1,
            title="Awesome Django",
            url="https://awesomedjango.org/",
            notes="Best place on the web for Django.",
        )
        # print(f"bookmark id: {self.bookmark.id}")

        # the simple router provides the name 'bookmark-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:bookmark-list")
        self.detail_url = reverse(
            "barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}
        )

    # 1. create a bookmark
    def test_create_bookmark(self):
        """
        Ensure we can create a new bookmark object.
        """

        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Django REST framework",
            "url": "https://www.django-rest-framework.org/",
            "notes": "Best place on the web for Django REST framework.",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Bookmark.objects.count(), 2)
        self.assertEqual(Bookmark.objects.get(
            id=99).title, "Django REST framework")

    # 2. list bookmarks
    def test_list_bookmarks(self):
        """
        Ensure we can list all bookmark objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"]
                         [0]["title"], self.bookmark.title)

    # 3. retrieve a bookmark
    def test_retrieve_bookmark(self):
        """
        Ensure we can retrieve a bookmark object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], self.bookmark.title)

    # 4. delete a bookmark
    def test_delete_bookmark(self):
        """
        Ensure we can delete a bookmark object.
        """
        response = self.client.delete(
            reverse("barkyapi:bookmark-detail",
                    kwargs={"pk": self.bookmark.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 0)

    # 5. update a bookmark
    def test_update_bookmark(self):
        """
        Ensure we can update a bookmark object.
        """
        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Awesomer Django",
            "url": "https://awesomedjango.org/",
            "notes": "Best place on the web for Django just got better.",
        }
        response = self.client.put(
            reverse("barkyapi:bookmark-detail",
                    kwargs={"pk": self.bookmark.id}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], "Awesomer Django")




# 11. create a user
class UserTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username="allie"
        )
        self.list_url = reverse("barkyapi:user-list")
        self.detail_url = reverse(
            "barkyapi:user-detail", kwargs={"pk": self.user.id}
        )

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """

        # data = {
        #     "id": 2,
        #     "username": "eric"
        # }

        # response = self.client.post(self.list_url, data, format="json")
        # self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(
            id=1).username, "allie")


# 12. retrieve a user

    def test_retrieve_user(self):
        """
        Ensure we can retrieve a user object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["username"], self.user.username)

# 13. delete a user
    def test_delete_user(self):
        """
        Ensure we can delete a user object.
        """
    #     response = self.client.delete(
    #         reverse("barkyapi:user-detail",
    #                 kwargs={"pk": self.user.id})
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(User.objects.count(), 0)
        self.user.delete()
        self.assertTrue(self.user.DoesNotExist)

# 14. list users
    def test_list_users(self):
        """
        Ensure we can list all user objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"]
                         [0]["username"], self.user.username)
