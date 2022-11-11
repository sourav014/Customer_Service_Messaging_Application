from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.create_user, name='create_user'), 
    path('update/<int:id>/', views.update_user, name='update_user'),
    path('list/', views.list_users, name='list_users'),
    path('<int:id>/', views.single_user,  name='single_user'),
    path('populate/user_data/', views.populate_user_data, name='populate_user_data')
]