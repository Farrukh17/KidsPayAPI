from django.urls import path
from . import views

app_name = 'core-api'

urlpatterns = [
    path('children/', views.ChildListView.as_view(), name='children_list'),
    path('child-detail/', views.ChildDetail.as_view(), name='child')
]
