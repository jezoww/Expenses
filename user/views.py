from random import randint

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView

from user.models import User
from user.serializers import RegisterModelSerializer, RegisterCheckSerializer
from user.tasks import send_email


@extend_schema(tags=['auth'], request=RegisterModelSerializer)
class RegisterAPIView(APIView):
    def post(self, request):
        # User.objects.filter(email='ismoilov000d@gmail.com').update(password=make_password('Jezow2008!'))
        s = RegisterModelSerializer(data=request.data)
        user = User.objects.filter(email=request.data.get("email")).first()
        if s.is_valid() or (user and not user.is_active):
            if not user:
                u = s.save()
                u.is_active = False
                u.save()
            code = randint(100000, 999999)
            email = request.data.get('email')
            send_email.delay(to_send=email, code=code)
            response = JsonResponse({"message": "Code send to your email!"}, status=HTTP_200_OK)
            response.set_cookie('code', make_password(str(code)), max_age=300)
            return response
        elif user and user.is_active:
            return JsonResponse({"message": "User with this email already registered!"}, status=HTTP_400_BAD_REQUEST)
        return JsonResponse(s.errors)

@extend_schema(tags=['auth'], request=RegisterCheckSerializer)
class RegisterCheckAPIView(APIView):
    def post(self, request):
        data = request.data.copy()
        verify_code = request.COOKIES.get('code')
        if not verify_code:
            return JsonResponse({"message": "Code expired!"}, status=HTTP_400_BAD_REQUEST)
        data['verify_code'] = verify_code
        s = RegisterCheckSerializer(data=data)
        if s.is_valid():
            User.objects.filter(email=data.get('email')).update(is_active=True)
            return JsonResponse({"message": "Successfully registered!", "status": 200}, status=HTTP_201_CREATED)
        return JsonResponse(s.errors)
