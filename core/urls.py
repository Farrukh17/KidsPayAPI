from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('^/api/getChildInfo/$', views.get_child_info)
]
