import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework.test import APIClient

from finance.choices import ExpenseTypeChoice
from finance.models import Category
from user.models import User


@pytest.mark.django_db
class TestAdmin:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def token1(self, client, db):
        url = reverse('token_obtain_pair')

        data = {"email": "1@gmail.com", "password": "Jezow2000!"}

        response = client.post(url, data)
        return response.data.get("access")

    @pytest.fixture
    def token2(self, client, db):
        url = reverse('token_obtain_pair')

        data = {"email": "2@gmail.com", "password": "Jezow2000!"}

        response = client.post(url, data)
        return response.data.get("access")

    @pytest.fixture
    def db(self):
        User.objects.create(fullname='ghj', email='1@gmail.com', password=make_password('Jezow2000!'), is_staff=True,
                            is_superuser=True)
        User.objects.create(fullname='ghj', email='2@gmail.com', password=make_password('Jezow2000!'))
        Category.objects.create(name='fds', type=ExpenseTypeChoice.LOSS)

    def test_create(self, client, db, token1, token2):
        url = reverse('category-create')

        data = {
            'name': 'gfds',
            'type': 'loss'
        }

        response = client.post(url, data, headers={"Authorization": "Bearer " + token1})

        assert response.status_code == 201

        response = client.post(url, data, headers={"Authorization": "Bearer " + token2})

        assert response.status_code == 403

        response = client.post(url, data)

        assert response.status_code == 401

    def test_update(self, client, db, token1, token2):
        url = reverse('category-update', kwargs={'pk': 1})

        data = {
            'name': 'hgfdsfgh',
            'type': 'loss'
        }

        response = client.patch(url, data, headers={"Authorization": "Bearer " + token1})

        assert response.status_code == 200

        response = client.patch(url, data, headers={"Authorization": "Bearer " + token2})

        assert response.status_code == 403

        response = client.patch(url, data)

        assert response.status_code == 401

    def test_delete(self, client, db, token1, token2):
        url = reverse('category-delete', kwargs={'pk': 1})

        response = client.post(url, headers={"Authorization": "Bearer " + token1})

        assert response.status_code == 200

        response = client.post(url, headers={"Authorization": "Bearer " + token1})

        assert response.status_code == 404

        response = client.post(url, headers={"Authorization": "Bearer " + token2})

        assert response.status_code == 403



        response = client.post(url)

        assert response.status_code == 401




