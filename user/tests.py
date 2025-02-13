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
        User.objects.create(fullname='Test', phone='+998991001143', password=make_password('Jezow2000!'))

    def test_register(self, client):
        url = reverse('register')
        data = {"fullname": "dfghj", "phone": "+998999999999", "password": "Jezow2000!"}

        response = client.post(url, data)

        assert response.status_code == 200

        # --------------------------------------

        response = client.post(url, data)

        assert response.status_code == 400

    def test_login(self, client, db):
        url = reverse('token_obtain_pair')

        data = {"phone": "+998991001143", "password": "Jezow2000!"}

        response = client.post(url, data)

        assert response.status_code == 200

        # --------------------------------------

        data = {'phone': '7894651', 'password': 'fff'}

        response = client.post(url, data)

        assert response.status_code == 401


