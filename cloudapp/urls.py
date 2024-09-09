from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('delete_file/<int:id>/', views.delete_file, name='delete_file'),
    path('', views.file_list, name='file_list'),
    path('signup/', views.signup, name='signup'),
    path('signup/details/', views.signup_details, name='signup_details'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('download/<int:document_id>/', views.download_file, name='download_file'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('folder/<int:folder_id>/', views.folder_view, name='folder_view'),
    path('move_document/<int:document_id>/', views.move_document_to_folder, name='move_document'),
    path('move_document_api/<int:document_id>/to_folder/<int:folder_id>/', views.move_document_to_folder_api, name='move_document_to_folder_api'),
    path('upload_folder/', views.upload_folder, name='upload_folder'),  # 폴더 업로드 URL 추가
]
