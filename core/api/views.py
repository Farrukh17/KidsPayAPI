from rest_framework import generics
from ..models import Child
from .serializers import ChildSerializer


class ChildListView(generics.ListAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer


class ChildDetailView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
