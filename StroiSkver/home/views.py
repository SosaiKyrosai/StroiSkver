from django.http import HttpResponse
from django.shortcuts import render
from .models import paper
from django.shortcuts import redirect


# Create your views here.
def index (request):
    papers = paper.objects.order_by('-id')  # тут_потом_сделать_минус_перед_айди
    return render(request,'Home/Home.html',{'title': 'Главная', 'papers': papers})
