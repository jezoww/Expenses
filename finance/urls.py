from django.urls import path

from finance.views import CategoryListAPIView, KirimChiqimCreateAPIView, KirimChiqimUpdateAPIView, KirimChiqimListAPIView, \
    TotalAPIView, KirimChiqimDestroyAPIView, KirimChiqimRetrieveAPIView

urlpatterns = [
    path('category/list/', CategoryListAPIView.as_view(), name='category-list'),
    path('kirim-chiqim/create/', KirimChiqimCreateAPIView.as_view(), name='kirimchiqim-create'),
    path('kirim-chiqim/update/<int:pk>/', KirimChiqimUpdateAPIView.as_view(), name='kirimchiqim-update'),
    path('kirim-chiqim/delete/<int:pk>/', KirimChiqimDestroyAPIView.as_view(), name='kirimchiqim-delete'),
    path('kirim-chiqim/detail/<int:pk>/', KirimChiqimRetrieveAPIView.as_view(), name='kirimchiqim-detail'),
    path('expenses/', KirimChiqimListAPIView.as_view(), name='kirimchiqim-list'),
    path('total/', TotalAPIView.as_view(), name='total'),
]