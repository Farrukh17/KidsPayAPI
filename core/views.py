from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import *


@require_POST
def get_child_info(request):
    childID = request.POST.get('childID')
    if childID:
        try:
            child = Child.objects.get(id=childID)
            return JsonResponse({'child': child})
        except:
            pass
    return JsonResponse({'child': None})
