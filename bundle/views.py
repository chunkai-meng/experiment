from django.shortcuts import render

from .models import Bundle


def bundles_view(request):
    return render(request, 'bundles.html', {'bundles': Bundle.objects.all()})
