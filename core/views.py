from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from .models import Child, Group


class GroupFee(DetailView):
    model = Child

    def post(self, *args, **kwargs):
        group_id = self.request.POST['group_id']
        data = {}
        if group_id:
            group = get_object_or_404(Group, id=group_id)
            data['group_fee'] = group.fee
        return JsonResponse(data)
