from django.test import TestCase
from reguser.utils import generate_username

class GenerateUsernameTestCase(TestCase):
    def setUp(self):
        self.emails = [
            "me@example.com",
            "a@b.c",
            "b@domain.com",
            "a.nonymous@example.com",
            "name+tag@example.com",
            "name\@tag@example.com",
            "spaces\ are\ allowed@example.com",
            '"spaces may be quoted"@example.com',
            "!#$%&'+-/=.?^`{|}~@[1.0.0.127]",
            "!#$%&'+-/=.?^`{|}~@[IPv6:0123:4567:89AB:CDEF:0123:4567:89AB:CDEF]",
            "me(this is a comment)@example.com",
                ]

    def test_generated_usernames_are_valid(self):
        for email in self.emails:
            usernames = []
            for i in range(100):
                username = generate_username(email)
                self.assertTrue(len(username) > 1)
                self.assertTrue(len(username) < 30)
                self.assertNotIn(username, usernames)
                usernames.append(username)
