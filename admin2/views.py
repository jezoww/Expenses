from django.http import JsonResponse
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from admin2.permissions import AdminPermission
from admin2.serializers import CategoryModelSerializer
from finance.models import Category


@extend_schema(tags=['category'], request=CategoryModelSerializer, responses=CategoryModelSerializer)
class CategoryCreateAPIView(CreateAPIView):
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    permission_classes = IsAuthenticated, AdminPermission

@extend_schema(tags=['category'])
class CategoryUpdateAPIView(UpdateAPIView):
    lookup_field = 'pk'
    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    permission_classes = IsAuthenticated, AdminPermission

@extend_schema(tags=['category'])
@permission_classes([IsAuthenticated, AdminPermission])
class DeleteCategoryAPIView(APIView):
    def post(self, request, pk):
        category = Category.objects.filter(id=pk).first()
        if not category:
            return JsonResponse({"error": "Not found!"}, status=HTTP_404_NOT_FOUND)

        serialized_data = CategoryModelSerializer(instance=category).data

        category.delete()

        return JsonResponse(serialized_data)

