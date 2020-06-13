from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import TypyBiletow, MiejscaTransakcji, TypyUlgi, MetodyPlatnosci
import datetime


def index(request):
    places = MiejscaTransakcji.objects.all()
    context = {
        'places' : places
    }
    return render(request, template_name = "landingPage/selectType.html", context= context)

def card(request):
    all_tickets_types = TypyBiletow.objects.all()
    template = loader.get_template('landingPage/index.html')
    context = {
        'all_tickets_types':  all_tickets_types,
    }
    return render(request, template_name = "landingPage/cardTicket.html",context=context)

def zonesCarton(request):
    zones = TypyBiletow.objects.order_by().values('strefa').distinct()
    context = {
        'name': "Bilet kartonikowy",
        'zones': list(zones),
    }
    return render(request, template_name = "landingPage/selectZone.html", context= context)
def timeCarton(request, zone):
    time = TypyBiletow.objects.filter(czas_waznosci__lt=datetime.timedelta(days=4), strefa= zone)
    print(time)
    context = {
        'name': "Bilet kartonikowy",
        'time': list(time),
        'next': "{% url 'ztm_app:reductionCarton' %}"
    }
    return render(request, template_name = "landingPage/selectTime.html", context= context)

def reductionCarton(request):
    reduction = TypyUlgi.objects.all()
    context = {
        'name': "Bilet kartonikowy",
        'reduction': reduction
    }
    return render(request, template_name = "landingPage/selectReduction.html", context = context)

def confirmCarton(request):
    payment = MetodyPlatnosci.objects.all()
    context = {
        'payment': payment
    }
    return render(request, template_name = "landingPage/confirmCarton.html", context = context)
