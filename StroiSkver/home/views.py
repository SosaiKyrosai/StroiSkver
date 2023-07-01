from django.http import HttpResponse
from django.shortcuts import render
from .models import paper
from django.shortcuts import redirect


# Create your views here.
def index(request):
    papers = paper.objects.order_by('-id')  # тут_потом_сделать_минус_перед_айди
    return render(request, 'Home/Home.html',{'title': 'Главная', 'papers': papers})


def faq(request):
    return render(request, 'FAQ.html')


def search_papers(request):
    query = request.GET.get('q')
    papers = paper.objects.filter(title__icontains=query) | paper.objects.filter(textOfPaper__icontains=query) if query else None
    return render(request, 'search_results.html', {'papers': papers, 'query': query})
