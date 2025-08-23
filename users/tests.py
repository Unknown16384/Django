from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from .models import UserProfile

User = get_user_model()

def setUpModule():
    global users
    users = []
    for user_num in range(11):
        users.append(User.objects.create(username=f'test_user {user_num}'))
        UserProfile.objects.create(user=users[user_num], name=f'test_name {user_num}', family=f'test_family {user_num}')

def tearDownModule():
    User.objects.all().delete()
    UserProfile.objects.all().delete()

class UserViewTest(TestCase):

    def test_home_page(self):
        url = ''
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        context = UserProfile.objects.all().prefetch_related('skills', 'skills__skill', 'gallery')[:4]
        # так пойдет, или для проверки контекста мне надо создавать пользователей с навыками и картинками?
        self.assertEqual(list(response.context['users']), list(context))

    def test_user_list_page(self):
        url = '/all/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        context = UserProfile.objects.all().prefetch_related('skills', 'skills__skill', 'gallery')[:10]
        # как (и надо ли вообще) проверять пагинатор? он же вроде как базовый, то есть типа весь из себя провереный?
        self.assertEqual(list(response.context['users']), list(context))

    def test_user_id_page(self):
        auth_client = Client()
        auth_client.force_login(users[0])
        login_url = settings.LOGIN_URL
        url = '/1/'
        response_no_auth = self.client.get(url)
        response = auth_client.get(url)
        self.assertRedirects(response_no_auth, f'{login_url}?next={url}')
        self.assertEqual(response.status_code, 200)
        context = UserProfile.objects.prefetch_related('skills', 'skills__skill', 'gallery').select_related('user__desk').get(id=1)
        self.assertEqual(response.context['user'], context)
