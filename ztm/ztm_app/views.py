from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import TypyBiletow,Transakcje,NosnikiKartonikowe,Nieimienne, MiejscaTransakcji, TypyUlgi, MetodyPlatnosci
import datetime
import json


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

def transactionCarton(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        place = MiejscaTransakcji.object.get(id_miejsca_transakcji = int(body['place']))
        payment = MetodyPlatnosci.object.get(id_metody_platnosci = 1)
        transaction = Transakcje.objects.create(id_miejsca_transakcji=place, id_metody_platnosci = payment)
        print('transakcja', transaction)
        context = {
            'transaction': transaction,
        }

        pass
    elif request.method == 'PUT':

        pass
    elif request.method == 'GET':
        pass
    elif request.method == 'DELETE':
        pass
    return render(request, template_name = "landingPage/selectPayment.html", context= context)
def addTicket(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
    return null

def amount(request):
    return render(request, template_name ="landingPage/selectAmount.html")

def continueCarton(request):
    return render(request, template_name="landingPage/continueCarton.html")
