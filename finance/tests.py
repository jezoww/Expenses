import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework.test import APIClient

from finance.choices import ExpenseTypeChoice
from finance.models import Category, Expense
from user.models import User


@pytest.mark.django_db
class TestExpense:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def token(self, client, db):
        url = reverse('token_obtain_pair')

        data = {"email": "test@gmail.com", "password": "Jezow2000!"}

        response = client.post(url, data)
        return response.data.get("access")

    @pytest.fixture
    def db(self):
        user = User.objects.create(fullname='Test', email='test@gmail.com', password=make_password('Jezow2000!'))
        Category.objects.create(name='Test', image='images/categories/test.png')
        Expense.objects.create(money=500, description="fg", type='profit', category_id=1, user=user)

    def test_create(self, client, db, token):
        url = reverse('expense-create')
        data = {
            "money": "500",
            "description": "WEtgyhuj",
            "type": "profit",
            "category": 1
        }

        response = client.post(url, data, headers={"Authorization": "Bearer " + token})

        assert response.status_code == 201

    def test_delete(self, client, db, token):
        url = reverse('expense-delete', kwargs={"pk": 1})

        response = client.post(url, headers={"Authorization": "Bearer " + token})

        assert response.status_code == 200

        # --------------------------------------

        response = client.post(url, headers={"Authorization": "Bearer " + token})

        assert response.status_code == 404

    def test_update(self, client, db, token):
        url = reverse('expense-update', kwargs={'pk': 1})

        data = {'money': 1000.00}

        response = client.patch(url, data, headers={"Authorization": "Bearer " + token})

        assert response.status_code == 200
        assert response.data.get('money') == '1000.00'

        # --------------------------------------

        url = reverse('expense-update', kwargs={'pk': 11546})
        data = {'money': 1000.00}

        response = client.patch(url, data, headers={"Authorization": "Bearer " + token})

        assert response.status_code == 404

    def test_detail(self, client, db, token):
        url = reverse('expense-detail', kwargs={'pk': 1})

        response = client.get(url, headers={"Authorization": "Bearer " + token})

        assert response.status_code == 200

        # --------------------------------------

        url = reverse('expense-detail', kwargs={'pk': 5412})

        response = client.get(url, headers={"Authorization": "Bearer " + token})

        assert response.status_code == 404

    def test_list(self, client, db, token):
        url = reverse('expense-list')

        response = client.get(url, headers={"Authorization": "Bearer " + token})

        assert response.status_code == 200

    def test_total(self, client, db, token):
        url = reverse('total')

        response = client.get(url, headers={'Authorization': 'Bearer ' + token})

        assert response.status_code == 200


@pytest.mark.django_db
class TestCategory:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def token(self, client, db):
        url = reverse('token_obtain_pair')

        data = {"email": "test@gmail.com", "password": "Jezow2000!"}

        response = client.post(url, data)
        return response.data.get("access")

    @pytest.fixture
    def db(self):
        user = User.objects.create(fullname='Test', email='test@gmail.com', password=make_password('Jezow2000!'))
        Category.objects.create(name='Test', image='images/categories/test.png', type=ExpenseTypeChoice.LOSS)
        Expense.objects.create(money=500, description="fg", type='profit', category_id=1, user=user)

    def test_category_list(self, client, db):
        url = reverse('category-list')

        data = {
            'type': 'loss'
        }

        response = client.get(url, data)

        assert response.status_code == 200
        assert len(response.data) == 1

        data['type'] = 'profit'

        response = client.get(url, data)

        assert response.status_code == 200
        assert len(response.data) == 0
