from django.shortcuts import render

# Create your views here.


def plaster_calc(request):
    return render(request, 'plaster_calc.html')