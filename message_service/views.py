from django.shortcuts import render
from .models import Message
from user_service.models import User
import csv
from django.utils import timezone
from .controllers import create_new_query, update_query, fetch_query, fetch_assigned_messages_of_staff, respond_to_query

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['POST'])
def create_message(request):
    if request.method == 'POST':
        data = request.data
        query_data = create_new_query(data)
        
        if query_data:
            # notify to the staff that new query assigened to him
            pass
        else:
            # do nothing
            pass
        
        return Response(
            {
                'message': 'Query Received, We will resolve it soon.',
                'query_id': query_data.id
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

@api_view(['POST'])
def update_message(request, id):
    if request.method == 'POST':
        data = request.data
        query_data = update_query(data, id)
        return Response(
            {
                'message': 'Query Updated.'
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
    

@api_view(['GET'])
def assigned_messages_of_staff(request):
    if request.method == 'GET':
        
        filter_params = {}

        if request.query_params.get('staff_id'):
            filter_params['staff_id'] = request.query_params.get('staff_id')
        
        if request.query_params.get('status'):
            filter_params['status'] = request.query_params.get('status')

        if request.query_params.get('priority'):
            filter_params['priority'] = request.query_params.get('priority')
    
        query_data = fetch_assigned_messages_of_staff(filter_params)
        return Response(
            {
                'Query': query_data
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

@api_view(['GET'])
def view_message(request, id):
    if request.method == 'GET':
        data = request.data
        query_data = fetch_query(id)
        return Response(
            {
                'Query': query_data
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

@api_view(['GET'])
def populate_message_data(request):
    if request.method == 'GET':
        with open('./GeneralistRails_Project_MessageData.csv', mode ='r')as file:
            csvFile = csv.reader(file)
            for lines in csvFile:
                message = {}
                if lines[0] != 'User ID':
                    try:
                        user_instance = User.objects.get(pk=int(lines[0]))
                    except User.DoesNotExist:
                        user_instance = None

                    message['user'] = user_instance

                if lines[1] != 'Timestamp (UTC)':
                    if lines[1]:
                        message['created_at'] = lines[1]
                        message['updated_at'] = lines[1]
                    else:
                        message['created_at'] = timezone.now()
                        message['updated_at'] = timezone.now()

                if lines[2] != 'Message Body':
                    message['message_text'] = lines[2]

                if message.get('user') is not None:
                    Message.objects.create(**message)

        return Response(
            {
                'message': 'Message Data Populated Successfully!'
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

@api_view(['POST'])
def respond_to_message_by_staff(request):
    if request.method == 'POST':
        data = request.data
        query_data = respond_to_query(data)
        return Response(
            {
                'message': 'Staff has responded to the user.'
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
