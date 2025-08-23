from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Desks
from users.models import UserProfile

User = get_user_model()

class DeskModelCleanTest(TestCase):

    def setUp(self):
        user = User.objects.create(username=f'test_user1')
        self.user2 = User.objects.create(username=f'test_user2')
        UserProfile.objects.create(user=user, name=f'test_name', family=f'test_family', tester=True)
        UserProfile.objects.create(user=self.user2, name=f'test_name2', family=f'test_family2')
        self.tester_desk = 3
        Desks.objects.create(user=user, number=self.tester_desk)

    def tearDown(self):
        User.objects.all().delete()
        UserProfile.objects.all().delete()
        Desks.objects.all().delete()

    def test_tester_and_developer_nearby(self):
        neigh1 = Desks(user=self.user2, number=self.tester_desk - 1)
        neigh2 = Desks(user=self.user2, number=self.tester_desk + 1)
        with self.assertRaises(ValidationError) as cm:
            neigh1.full_clean()
        self.assertIn("'Тестировщики и разработчики не должны сидеть за соседними столами.", str(cm.exception))
        with self.assertRaises(ValidationError) as cm:
            neigh2.full_clean()
        self.assertIn("'Тестировщики и разработчики не должны сидеть за соседними столами.", str(cm.exception))
