from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader

from .models import TypyBiletow,Transakcje,NosnikiKartonikowe,Nieimienne, MiejscaTransakcji, TypyUlgi, MetodyPlatnosci,  NosnikiElektroniczne, Imienne,Ulgi

import datetime
import json


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
def timeCarton(request):
    time = TypyBiletow.objects.filter(czas_waznosci__lt=datetime.timedelta(days=4))
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

    return render(request, template_name = "landingPage/selectPayment.html", context = context)

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

    

def transactionCarton(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        place = MiejscaTransakcji.object.get(id_miejsca_transakcji = int(body['place']))
        payment = MetodyPlatnosci.object.get(id_metody_platnosci = body['payment'])
        ticketType = TypyBiletow.object.get(id_typu = body['type'])
        reduction = TypyUlgi.object.get(id_typu_ulgi = body['reduction'])
        transaction = Transakcje.objects.create(id_miejsca_transakcji=place, id_metody_platnosci = payment)
        cartonTicket = NosnikiKartonikowe.objects.create(kod=random.randint(1,100000000))
        ticket = Nieimienne.object.create(id_transakcji=transaction, id_nosnika= cartonTicket,id_typu= ticketType,id_typu_ulgi=reduction)
        print('transakcja', transaction, cartonTicket, ticket)
        context = {
            'transaction': transaction,
            'payment': payment,
            'ticketType': ticketType,
            'reduction': reduction
        }

        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'GET':
        pass
    elif request.method == 'DELETE':
        pass
    return render(request, template_name = "landingPage/selectPayment.html", context= context)
