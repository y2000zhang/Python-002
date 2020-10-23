from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from . import models


from .models import Shortcuts
# from django.db.models import Avg


def short(request):
    shorts = Shortcuts.objects.all()
    print("short:", shorts)
    condtions = {'n_star__gte': 3}
    plus = shorts.filter(**condtions)
    print("plus:", plus)

    return render(request, 'index.html', locals())
