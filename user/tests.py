import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework.test import APIClient

from user.models import User


@pytest.mark.django_db
class TestAuth:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def db(self):
        User.objects.create(fullname='Test', email='test@gmail.com', password=make_password('Jezow2000!'))

    def test_register(self, client):
        url = reverse('register')
        data = {"fullname": "dfghj", "email": "fghj@gmail.com", "password": "Jezow2000!"}

        response = client.post(url, data)

        assert response.status_code == 200

        # --------------------------------------

        # response = client.post(url, data)
        #
        # assert response.status_code == 400

    def test_login(self, client, db):
        url = reverse('token_obtain_pair')

        data = {"email": "test@gmail.com", "password": "Jezow2000!"}

        response = client.post(url, data)

        assert response.status_code == 200

        # --------------------------------------

        data = {'email': 'ghj@gmail.com', 'password': 'fff'}

        response = client.post(url, data)

        assert response.status_code == 401
