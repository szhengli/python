from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [ path('', views.index, name='index') ,
                path('<int:question_id>/', views.detail, name='detail'),
                path('<int:question_id>/results/', views.results, name='results'),
                path('<int:question_id>/vote/', views.vote, name='vote'),
                path('login/', views.auths, name='login'),
                path('profiles/', views.Profiles.as_view(), name='profiles'),
                path('lists/' , views.PubliserList.as_view()),
                path('test/' , views.test_js),
                path('progress/' , views.progress , name='progress'),
                path('progress_front/' , views.progress_front, name='progress_front'),
                path('deploy_backend/', views.deploy_backend, name='deploy_backend'),
                path('deploy_frontend/', views.deploy_frontend, name='deploy_frontend'),
                path('locked_user/' , views.locked_user , name='locked_user'),
                path('unlock/' , views.unlock , name='unlock'),
                ]


