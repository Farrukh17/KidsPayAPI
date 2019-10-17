from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path(r'get_group_fee/', views.GroupFee.as_view(), name='get_group_fee')
]
