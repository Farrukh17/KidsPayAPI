from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('children/', views.ChildListView.as_view(), name='children_list'),
    path('child/<id>/', views.ChildDetailView.as_view(), name='child_detail')
]
