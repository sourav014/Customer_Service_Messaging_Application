from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.create_message, name='create_message'), 
    path('update/<int:id>/', views.update_message, name='update_message'),
    path('list/', views.assigned_messages_of_staff, name='list_messages'),
    path('<int:id>/', views.view_message,  name='view_message'),
    path('respond/message/', views.respond_to_message_by_staff,  name='respond_message'),
    path('populate/message_data/', views.populate_message_data, name='populate_message_data')
]