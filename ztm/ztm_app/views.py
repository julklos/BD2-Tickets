from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import TypyBiletow


def index(request):
    return render(request, template_name = "landingPage/selectType.html")

def card(request):
    all_tickets_types = TypyBiletow.objects.all()
    print(all_tickets_types)
    template = loader.get_template('landingPage/index.html')
    context = {
        'all_tickets_types':  all_tickets_types,
    }
    return render(request, template_name = "landingPage/cardTicket.html",context=context)

def carton(request):

    return render(request, template_name = "landingPage/cartonTicket.html")

