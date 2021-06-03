from django.test import TestCase

from .models import Game

# Create your tests here.

class GameModelTests(TestCase):

    def test_sample(self):
        a = "hi"
        b = "there"
        self.assertEqual(a,b)