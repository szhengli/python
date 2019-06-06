from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [ path('', views.index, name='index') ,

                path('login/', views.auths, name='login'),
                path('profiles/', views.Profiles.as_view(), name='profiles'),
                path('test/' , views.test_js),
                path('progress/' , views.progress , name='progress'),
                path('progress_front/' , views.progress_front, name='progress_front'),
                path('deploy_backend/', views.deploy_backend, name='deploy_backend'),
                path('deploy_frontend/', views.deploy_frontend, name='deploy_frontend'),
                path('locked_user/' , views.locked_user , name='locked_user'),
                path('unlock/' , views.unlock , name='unlock'),
                path('deploy_logs/' , views.deploy_logs, name='deploy_logs'),
                path('logouts/', views.logouts, name='logouts'),
                ]


