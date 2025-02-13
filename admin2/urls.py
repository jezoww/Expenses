from django.urls import path

from admin2.views import CategoryCreateAPIView, CategoryUpdateAPIView, DeleteCategoryAPIView

urlpatterns = [
    path('categiory-create/', CategoryCreateAPIView.as_view(), name='category-create'),
    path('categiory-update/<int:pk>', CategoryUpdateAPIView.as_view(), name='category-update'),
    path('categiory-delete/<int:pk>', DeleteCategoryAPIView.as_view(), name='category-delete')
]
