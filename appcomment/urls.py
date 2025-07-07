from django.urls import path
from django.shortcuts import redirect

from . import views

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('logout/', views.logout_view, name='logout'),
    path ('login/', views.login_view, name='login'),
    path('registration/', views.register_view, name='register'),
    path('main_list/', views.main_list_view, name='main_list'),
    path('delete/<int:id_entry>', views.delete_view, name = 'delete'),
    path('update/<int:id_entry>', views.update_view, name = 'update'),
    path('add_comment/<int:id_entry>', views.add_comment, name = 'add_comment'),
    path('like_comment/', views.like_comment, name = 'like_comment')
]