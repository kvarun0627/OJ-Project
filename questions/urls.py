# questions/urls.py
from django.urls import path
from . import views
from compiler import views as compiler_views
urlpatterns = [
    path('', views.question_lists, name='question_list'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
    path('create/', views.create_question, name='question_create'),
    path('<int:pk>/edit/', views.update_question, name='question_update'),
    path('<int:pk>/delete/', views.delete_question, name='question_delete'),
    path('<int:pk>/submission',compiler_views.question_submissions,name='submission'),
    path('<int:pk>/submission/<int:submission_id>/test_result/',compiler_views.testcase_results,name='testcase_results')
]
