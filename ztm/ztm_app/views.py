from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import TypyBiletow, MiejscaTransakcji, TypyUlgi, MetodyPlatnosci, NosnikiElektroniczne, Imienne, TypyUlgi, Ulgi
import datetime


def index(request):
    places = MiejscaTransakcji.objects.all()
    context = {
        'places' : places
    }
    return render(request, template_name = "landingPage/selectType.html", context= context)

def selectCard(request):
    context = {
        'name':  "Doladowanie karty",
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

def selectZoneTicket(request):
    id_t = request.POST.get('id_t')
    print(id_t)
    try:
        user_card = NosnikiElektroniczne.objects.get(id_nosnika=id_t)
    except:
        return render(request, template_name = "landingPage/invalidId.html")
    
    user_ticket = list(Imienne.objects.filter(id_nosnika = id_t).order_by('-data_waznosci'))
    user_ulga = Ulgi.objects.get(id_ulgi = user_card.id_ulgi)
    if user_ticket[0].data_waznosci is not None and user_ticket[0].data_waznosci > datetime.date.today():
        contex = {
        'name':  "Doladowanie karty",
        'cardId' : user_card,
        'ticket' : user_ticket[0],
        'ulga' : user_ulga,
        }
        return render(request, "landingPage/ticketExist.html", context = contex)

    zones = TypyBiletow.objects.order_by().values('strefa').distinct()
    contex = {
        'name':  "Doladowanie karty",
        'cardId' : user_card,
        'ticket' : user_ticket[0],
        'ulga' : user_ulga,
        'zones': list(zones),
    }
    return render(request, template_name = "landingPage/selectCardZone.html", context = contex)

    

    
