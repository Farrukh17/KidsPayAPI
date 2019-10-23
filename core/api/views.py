from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from ..models import Child, App
from .serializers import ChildSerializer, TransactionSerializer
from finance.models import Transaction


def check_request(request):
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
            return Response(data={'error': '{app} не имеет доступа к серивису KidsPay'.format(app=appName)},
                            status=status.HTTP_400_BAD_REQUEST)
        if app.status != 'active':
            return Response(data={'error': 'Статус вашего запроса пассивный! '
                                           'Пожалуйста обратитесь к администратору KidsPay'},
                            status=status.HTTP_400_BAD_REQUEST)

        if app.token != token:
            return Response(
                data={'error': 'Неавторизованный доступ. Несоответвующий токен для {app}'.format(app=appName)},
                status=status.HTTP_401_UNAUTHORIZED)
        return app
    else:
        return Response(data={'error': 'В Header запроса отсутсвуют TOKEN или APP'},
                        status=status.HTTP_400_BAD_REQUEST)


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

        check_request(request)

        if childID is not '' and schoolID is not '':
            id_child = schoolID.zfill(5) + ':' + childID.zfill(4)
            child = get_object_or_404(self.get_queryset(), id=id_child)
            child_serializer = self.get_serializer(child)
            return Response(child_serializer.data)
        else:
            return Response({'error': 'Отсутвуют параметры: childId={childId}, schoolID={schoolId}'.format(childId=childID, schoolId=schoolID)}, status=status.HTTP_400_BAD_REQUEST)


class TransactionsListCreate(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        # implement logic here
        return Transaction.objects.all()

    def post(self, request, *args, **kwargs):
        self.app = check_request(request)
        return super(TransactionsListCreate, self).post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if request.data.get('transactions'):
            for transaction in request.data.get('transactions'):
                transaction['school'] = str(transaction.get('school', '')).zfill(5)
                transaction['child'] = transaction['school'] + ':' + str(transaction.get('child', '')).zfill(4)
                serializer = self.get_serializer(data=transaction)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def perform_create(self, serializer):
        transaction = serializer.save(appType=self.app, paymentMethod=Transaction.PAYMENT_METHODS[0][0])
        transaction.child.balance += transaction.amount
        transaction.child.save()




