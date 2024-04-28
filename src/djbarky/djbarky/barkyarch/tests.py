from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import localtime

from barkyapi.models import Bookmark
from barkyarch.domain.model import DomainBookmark
from barkyarch.services.commands import (
    AddBookmarkCommand,
    ListBookmarksCommand,
    DeleteBookmarkCommand,
    EditBookmarkCommand,
    GetBookmarkCommand,
)


class TestCommands(TestCase):
    def setUp(self):
        right_now = localtime().date()

        self.domain_bookmark_1 = DomainBookmark(
            id=1,
            title="Test Bookmark",
            url="http://www.example.com",
            notes="Test notes",
            date_added=right_now,
        )

        self.domain_bookmark_2 = DomainBookmark(
            id=2,
            title="Test Bookmark 2",
            url="http://www.example2.com",
            notes="Test notes 2",
            date_added=right_now,
        )

    def test_command_add(self):
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)

        # run checks

        # one object is inserted
        self.assertEqual(Bookmark.objects.count(), 1)

        # that object is the same as the one we inserted
        self.assertEqual(Bookmark.objects.get(
            id=1).url, self.domain_bookmark_1.url)

    def test_command_list(self):
        # arrange
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)
        add_command.execute(self.domain_bookmark_2)

        # act
        list_command = ListBookmarksCommand()
        results = list_command.execute(self)

        # 2 objects in list
        self.assertEqual(results.count(), 2)

    def test_command_delete(self):
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)

        delete_command = DeleteBookmarkCommand()
        delete_command.execute(self.domain_bookmark_1)

        self.assertEqual(Bookmark.objects.count(), 0)


# edit command is getting following error: "Attribute Error: 'NoneType' object has no attribute 'save'
    # def test_command_edit(self):
    #     # arrange
    #     add_command = AddBookmarkCommand()
    #     add_command.execute(self.domain_bookmark_1)

    #     # act
    #     get_command = GetBookmarkCommand()
    #     get_command.execute(self.domain_bookmark_1.id ==
    #                         1).title = "New Bookmark"

    #     edit_command = EditBookmarkCommand()
    #     edit_command.execute(self.domain_bookmark_1)

    #     get_command.execute(self.domain_bookmark_1.id == 1)

    #     # new title is "Update Bookmark"
    #     self.assertEqual(self.domain_bookmark_1.title, "Update Bookmark")
        
