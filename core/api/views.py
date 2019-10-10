from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from ..models import Child
from .serializers import ChildSerializer


class ChildListView(generics.ListAPIView):
    queryset = Child.objects.filter(group=1, school=12)
    serializer_class = ChildSerializer


class ChildDetail(generics.GenericAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        childID = request.data.get('childID', None)
        schoolID = request.data.get('schoolID', None)
        if childID and schoolID:
            id_child = schoolID + ':' + childID
            child = get_object_or_404(self.get_queryset(), id=id_child)
            child_serializer = self.get_serializer(child)
            return Response({'child': child_serializer.data})
        return Response({'child': None})
