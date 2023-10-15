from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('daraja/stk-push', views.stk_push_callback, name='mpesa_stk_push_callback'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('users/', views.view_all_users, name='view_all_users'),
 


]