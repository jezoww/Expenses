from django.urls import path

from finance.views import CategoryListAPIView, ExpenseCreateAPIView, ExpenseUpdateAPIView, ExpenseListAPIView, \
    TotalAPIView, ExpenseDestroyAPIView, ExpenseRetrieveAPIView

urlpatterns = [
    path('category/list', CategoryListAPIView.as_view(), name='category-list'),
    path('expenses/create', ExpenseCreateAPIView.as_view(), name='expense-create'),
    path('expenses/update/<int:pk>', ExpenseUpdateAPIView.as_view(), name='expense-update'),
    path('expenses/delete/<int:pk>', ExpenseDestroyAPIView.as_view(), name='expense-delete'),
    path('expenses/detail/<int:pk>', ExpenseRetrieveAPIView.as_view(), name='expense-detail'),
    path('expenses', ExpenseListAPIView.as_view(), name='expense-list'),
    path('total', TotalAPIView.as_view(), name='total'),
]