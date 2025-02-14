from django.urls import path

from admin2.views import CategoryCreateAPIView, CategoryUpdateAPIView, DeleteCategoryAPIView

urlpatterns = [
    path('category', CategoryCreateAPIView.as_view(), name='category-create'),
    path('category/<int:pk>', CategoryUpdateAPIView.as_view(), name='category-update'),
    path('category-delete/<int:pk>', DeleteCategoryAPIView.as_view(), name='category-delete')
]
