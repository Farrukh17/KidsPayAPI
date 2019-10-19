from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from ..models import Child, App
from .serializers import ChildSerializer


class ChildListView(generics.ListAPIView):
    queryset = Child.objects.filter(group=1, school=12)
    serializer_class = ChildSerializer


class ChildDetail(generics.GenericAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        childID = str(request.data.get('childID', ''))
        schoolID = str(request.data.get('schoolID', ''))
        token = request.META.get('HTTP_TOKEN', None)
        appName = request.META.get('HTTP_APP', None)
        if appName and token:
            try:
                app = App.objects.get(name=appName)
            except ObjectDoesNotExist:
                app = None
            except MultipleObjectsReturned:
                app = None

            if not app:
                return Response(data={'error': '{app} не имеет доступа к серивису KidsPay' .format(app=appName)}, status=400)
            if app.status != 'active':
                return Response(data={'error': 'Статус вашего запроса пассивный! '
                                               'Пожалуйста обратитесь к администратору KidsPay'}, status=400)

            if app.token != token:
                return Response(data={'error': 'Неавторизованный доступ. Несоответвующий токен для {app}' .format(app=appName)}, status=401)
        else:
            return Response(data={'error':'В Header запроса отсутсвуют TOKEN или APP'}, status=400)

        if childID is not '' and schoolID is not '':
            id_child = schoolID.zfill(5) + ':' + childID.zfill(4)
            child = get_object_or_404(self.get_queryset(), id=id_child)
            child_serializer = self.get_serializer(child)
            return Response(child_serializer.data)
        else:
            return Response({'error': 'Отсутвуют параметры: childId={childId}, schoolID={schoolId}'.format(childId=childID, schoolId=schoolID)}, status=400)

