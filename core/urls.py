from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('getChildInfo/', views.get_child_info)
]
