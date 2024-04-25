from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from .serializer import UserSerializer
from rest_framework.response import Response


class UserView(APIView):
    def get(self, request):
        output = [
            {
                "email": output.email,
                "password": output.password,
                "first_name": output.first_name,
                "last_name": output.last_name,
                "phone": output.phone,
                "position": output.position,
                "user_id": output.user_id
            } for output in User.objects.all()
        ]
        return Response(output)

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)