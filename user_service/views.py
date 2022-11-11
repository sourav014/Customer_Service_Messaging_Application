from django.shortcuts import render
from .models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def create_user(request):
    pass

def update_user(request):
    pass


def list_users(request):
    pass

def single_user(request):
    pass

@api_view(['GET'])
def populate_user_data(request):
    if request.method == 'GET':
        i=1
        while i<=10000:
            first_name = f"branch{i}"
            last_name = f"international{i}"
            email = f"{first_name}.{last_name}@gmail.com"
            User.objects.create(
                first_name = first_name,
                last_name = last_name,
                email = email
            )
            i += 1

        return Response(
            {
                'message': 'User Data Populated Successfully!'
            }, 
            status=status.HTTP_200_OK
        )
        
    else:
        return Response(
            {
                'message': 'Method not allowed'
            }, 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

