from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader

from .models import TypyBiletow,Transakcje,NosnikiKartonikowe,Nieimienne, MiejscaTransakcji, TypyUlgi, MetodyPlatnosci,  NosnikiElektroniczne, Imienne,Ulgi, TypyNosnikow, Pasazerowie

import datetime
import json
import random

from ztm_app.forms import ConcessionForm, CardTypeForm, DeleteCardTypeForm, DeleteConcessionForm, UpdateConcessionForm, UpdateCardTypeForm

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

def selectTicket(request):
    context = {
        'name':  "Aktywuj bilet",
    }
    return render(request, template_name = "landingPage/activationTicket.html",context=context)

def zonesCarton(request):
    zones = TypyBiletow.objects.order_by().values('strefa').distinct()
    context = {
        'name': "Bilet kartonikowy",
        'zones': list(zones),
    }
    return render(request, template_name = "landingPage/selectZone.html", context= context)

def timeCarton(request, zone):
    time = TypyBiletow.objects.filter(czas_waznosci__lt=datetime.timedelta(days=4), strefa = zone)
    context = {
        'name': "Bilet kartonikowy",
        'time': list(time),
        'next': "{% url 'ztm_app:reductionCarton' %}"
    }
    return render(request, template_name = "landingPage/selectTime.html", context= context)

def selectTicketCarton(request):
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

def confirmCard(request):
    payment = MetodyPlatnosci.objects.all()
    context = {
        'payment': payment
    }

    return render(request, template_name = "landingPage/selectPaymentCard.html", context = context)

def findTicket(request):
    id_b = request.POST.get('id_b')
    print(id_b)
    user_ticket = Imienne.objects.filter(id_biletu = id_b)
    if user_ticket == None:
        user_ticket = Nieimienne.objects.filter(id_biletu = id_b)
        if user_ticket == None:
            return render(request, "landingPage/invalidTicketId.html")
    if user_ticket[0].data_aktywacji is not None:
        return render(request, "landingPage/ticketActivated.html")
    user_type = TypyBiletow.objects.get(id_typu_biletu = user_ticket[0].id_typu)
    
    contex = {
        'name' : "Aktywuj bilet",
        'ticket' : user_ticket[0],
        'type' : user_type,
    }
    return render(request, template_name = "landingPage/activate.html", context = contex)

def selectZoneTicket(request):
    id_t = request.POST.get('id_t')
    print(id_t)
    try:
        user_card = NosnikiElektroniczne.objects.get(id_nosnika=id_t)
    except:
        return render(request, template_name = "landingPage/invalidId.html")
    
    user_ticket = list(Imienne.objects.filter(id_nosnika = id_t).order_by('-data_waznosci'))
    user_ulga = Ulgi.objects.get(id_ulgi = user_card.id_ulgi)
    if user_ticket[0].data_waznosci is not None and user_ticket[0].data_waznosci > datetime.date.today(): # DO ZMIANY
        contex = {
        'name':  "Doladowanie karty",
        'cardId' : user_card,
        'ticket' : user_ticket[0],
        'ulga' : user_ulga,
        }
        return render(request, "landingPage/ticketExist.html", context = contex)
    
    if user_ulga.data_waznosci < datetime.date.today():
        contex = {
        'name':  "Doladowanie karty",
        'cardId' : user_card,
        'ticket' : user_ticket[0],
        'ulga' : user_ulga,
        }
        return render(request, "landingPage/reductionInvalid.html", context = contex)

    time = TypyBiletow.objects.filter(czas_waznosci__gte=datetime.timedelta(days=4)).order_by('-czas_waznosci')
    contex = {
        'name':  "Doladowanie karty",
        'cardId' : user_card,
        'ticket' : user_ticket[0],
        'ulga' : user_ulga,
        'time': list(time),
    }
    return render(request, template_name = "landingPage/selectCardZone.html", context = contex)

    

def transactionCarton(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(int(body['place']))
        place = MiejscaTransakcji.objects.get(id_miejsca_transakcji = int(body['place']))
        payment = MetodyPlatnosci.objects.get(id_metody_platnosci = body['payment'])
        transaction = Transakcje.objects.create(id_miejsca_transakcji=place, id_metody_platnosci = payment)
        for item in body['items']:
            reduction = TypyUlgi.objects.get(id_typu_ulgi = item['reduction'])
            typeTicket = TypyBiletow.objects.get(id_typu_biletu= item['type'])
            for i in range(1, int(item['amount'])+1):
                
                ticket = NosnikiKartonikowe.objects.create(kod = random.randint(1,1000000))
                ticketCarton = Nieimienne.objects.create(id_transakcji= transaction.id_transakcji, id_nosnika=ticket,id_typu=typeTicket.id_typu_biletu,id_typu_ulgi= reduction)

        #print('transakcja', transaction)
        # context = {
        #     'transaction': transaction,
        # }
        print(place, payment, body)
    elif request.method == 'PUT':
        pass
    elif request.method == 'GET':
        pass
    elif request.method == 'DELETE':
        pass
    return render(request, template_name='landingPage/thankYou.html')
    

def transactionCard(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(int(body['place']))
        place = MiejscaTransakcji.objects.get(id_miejsca_transakcji = int(body['place']))
        payment = MetodyPlatnosci.objects.get(id_metody_platnosci = body['payment'])
        transaction = Transakcje.objects.create(id_miejsca_transakcji=place, id_metody_platnosci = payment)
        for item in body['items']:
            reduction = Ulgi.objects.get(id_ulgi = item['reduction'])
            typeTicket = TypyBiletow.objects.get(id_typu_biletu= item['type'])
            client = Pasazerowie.objects.get(id_pasazera = item['client'])
            card = NosnikiElektroniczne.objects.get(id_nosnika = item['card'])
            ticket = Imienne.objects.create(id_transakcji= transaction.id_transakcji, id_nosnika=card.id_nosnika, id_pasazera = card,
                id_typu=typeTicket.id_typu_biletu,id_ulgi= reduction.id_ulgi)

        #print('transakcja', transaction)
        # context = {
        #     'transaction': transaction,
        # }
        print(place, payment, body)

        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'GET':
        pass
    elif request.method == 'DELETE':
        pass
    return render(request, template_name='landingPage/index.html')

def transactionActivation(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        user_ticket = Imienne.objects.filter(id_biletu = body['ticket'])
        if user_ticket == None:
            user_ticket = Nieimienne.objects.filter(id_biletu = body['ticket'])
        user_ticket[0].data_aktywacji = datetime.date.today()
        print(user_ticket[0].data_aktywacji)
        user_ticket[0].save()

        print(body)
        
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'GET':
        pass
    elif request.method == 'DELETE':
        pass
    return render(request, template_name='landingPage/index.html')

def addTicket(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
    return null

def amount(request):
    return render(request, template_name ="landingPage/selectAmount.html")

def continueCarton(request):
    return render(request, template_name="landingPage/continueCarton.html")

def thankYou(request):
    return render(request, template_name="landingPage/thankYou.html")

def end(request):
    return render(request, template_name="landingPage/end.html")
  
def reportPage(request):
    return render(request, template_name="reportPage/reportPage.html")

def editPage(request):
    return render(request, template_name="reportPage/editPage.html")

def statsPage(request):
    return render(request, template_name="reportPage/statsPage.html")

def addConcession(request):
    if request.method == 'POST':
        form = ConcessionForm(request.POST)
        if form.is_valid():
            TypyUlgi.objects.create(kod_podstawowy=form.cleaned_data['code'], wielkosc_ulgi=form.cleaned_data['discount'], nazwa=form.cleaned_data['name'])
            return render(request, template_name="reportPage/addingSuccess.html", context={'name': 'Typ Ulgi'})
    else:
        form = ConcessionForm()
        return render(request, template_name="reportPage/addConcession.html", context={'form': form})

def addCardType(request):
    if request.method == 'POST':
        form = CardTypeForm(request.POST)
        if form.is_valid():
            TypyNosnikow.objects.create(nazwa=form.cleaned_data['name'])
            return render(request, template_name="reportPage/addingSuccess.html", context={'name': 'Typ Nośnika'})
    else:
        form = CardTypeForm()
        return render(request, template_name="reportPage/addCardType.html", context={'form': form})

def deleteConcession(request):
    if request.method == 'POST':        
        form = DeleteConcessionForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            TypyUlgi.objects.filter(id_typu_ulgi=id).delete()
            return render(request, template_name="reportPage/deletingSuccess.html", context={'name': 'Typ Ulgi'})
    else:
        types = TypyUlgi.objects.all().values()
        form = DeleteConcessionForm()
    return render(request, template_name="reportPage/deleteConcession.html", context={'form': form, 'types': types})

def deleteCardType(request):
    if request.method == 'POST':        
        form = DeleteCardTypeForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            TypyNosnikow.objects.filter(id_typu_nosnika=id).delete()
            return render(request, template_name="reportPage/deletingSuccess.html", context={'name': 'Typ Nośnika'})
    else:
        types = TypyNosnikow.objects.all().values()
        form = DeleteCardTypeForm()
    return render(request, template_name="reportPage/deleteCardType.html", context={'form': form, 'types': types})

def updateConcession(request):
    if request.method == 'POST':
        form = UpdateConcessionForm(request.POST)
        if form.is_valid():
            concession = TypyUlgi.objects.get(id_typu_ulgi=form.cleaned_data['id'])
            if form.cleaned_data['code'] is not None:
                concession.kod_podstawowy = form.cleaned_data['code']
            if form.cleaned_data['discount'] is not None:
                concession.wielkosc_ulgi = form.cleaned_data['discount']
            if form.cleaned_data['name']:
                concession.nazwa = form.cleaned_data['name']
            concession.save()
        return render(request, template_name="reportPage/updateSuccess.html", context={'name': 'Typ Ulgi'})
    else:
        types = TypyUlgi.objects.all().order_by('id_typu_ulgi').values()
        form = UpdateConcessionForm()
        return render(request, template_name="reportPage/updateConcession.html", context={'form': form, 'types': types})

def updateCardType(request):
    if request.method == 'POST':
        form = UpdateCardTypeForm(request.POST)
        if form.is_valid():
            card_type = TypyNosnikow.objects.get(id_typu_nosnika=form.cleaned_data['id'])
            if form.cleaned_data['name']:
                card_type.nazwa = form.cleaned_data['name']
            card_type.save()
        return render(request, template_name="reportPage/updateSuccess.html", context={'name': 'Typ Nośnika'})
    else:
        types = TypyNosnikow.objects.all().order_by('id_typu_nosnika').values()
        form = UpdateCardTypeForm()
        return render(request, template_name="reportPage/updateCardType.html", context={'form': form, 'types': types})

