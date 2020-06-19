from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum
import django

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
    user_ticket = list(Imienne.objects.filter(id_biletu = id_b))
    if len(user_ticket) == 0:
        user_ticket = list(Nieimienne.objects.filter(id_biletu = id_b))
        if len(user_ticket) == 0:
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
    if user_ticket[0].data_waznosci is None or user_ticket[0].data_waznosci.date() > datetime.date.today(): # DO ZMIANY
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
        user_ticket = list(Imienne.objects.filter(id_biletu = body['ticket']))
        if len(user_ticket) == 0 :
            user_ticket = list(Nieimienne.objects.filter(id_biletu = body['ticket']))
        user_ticket[0].data_aktywacji = django.utils.timezone.now()
        print(user_ticket[0].data_aktywacji)
        print(datetime.date.today())
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
        
def statsPage(request):
    statistics = ['brak', 'Bilety', 'MiejscaTransakcji', 'Transakcje'];
    return render(request, template_name = "reportPage/statsPage.html", context = 
    {'statistics': statistics})

def ticketStats(request):
    numberOfElectronicTickets = Imienne.objects.filter().count()
    numberOfPaperTickets = Nieimienne.objects.filter().count()
    tickets = TypyBiletow.objects.all()
    tmp_k=0;
    liczba_biletow_k=0;    
    for ticket in tickets:
        tmp_k = Nieimienne.objects.filter(id_typu = ticket.id_typu_biletu).count()
        if tmp_k > liczba_biletow_k:
            liczba_biletow_k = tmp_k
            mostPopularPaperTicketId = ticket.id_typu_biletu

    e_procent = (numberOfElectronicTickets/(numberOfElectronicTickets+numberOfPaperTickets))*100
    e_procent = round(e_procent, 2)

    p_procent = (numberOfPaperTickets/(numberOfElectronicTickets+numberOfPaperTickets))*100
    p_procent = round(p_procent, 2)

    mostPopularPaperTicketProcent = (liczba_biletow_k/numberOfPaperTickets)*100
    mostPopularPaperTicketProcent = round(mostPopularPaperTicketProcent, 2)
    mostPopularPaperTicket = TypyBiletow.objects.filter(id_typu_biletu = mostPopularPaperTicketId)[0].czas_waznosci

    tmp_e=0;
    liczba_biletow_e=0;    
    for ticket in tickets:
        tmp_e = Imienne.objects.filter(id_typu = ticket.id_typu_biletu).count()
        if tmp_e > liczba_biletow_e:
            liczba_biletow_e = tmp_e
            mostPopularElectronicTicketId = ticket.id_typu_biletu

    mostPopularElectronicTicketProcent = (liczba_biletow_e/numberOfElectronicTickets)*100
    mostPopularElectronicTicketProcent = round(mostPopularElectronicTicketProcent, 2)
    mostPopularElectronicTicket = TypyBiletow.objects.filter(id_typu_biletu = mostPopularElectronicTicketId)[0].czas_waznosci

    conncessions = TypyUlgi.objects.all()
    tmp_u_n=0
    tmp_u_i=0
    tmp_u=0
    liczba_biletow_u=0;
    for concession in conncessions:
        if concession.id_typu_ulgi==7:
            break;
        tmp_u_n = Nieimienne.objects.filter(id_typu_ulgi = concession.id_typu_ulgi).count()
        tmp_u_i = Ulgi.objects.filter(id_typu_ulgi = concession.id_typu_ulgi).count()
        tmp_u = tmp_u_i+tmp_u_n
        if tmp_u > liczba_biletow_u:
            liczba_biletow_u = tmp_u
            mostPopularConcessionId = concession.id_typu_ulgi

    mostPopularConcession = TypyUlgi.objects.filter(id_typu_ulgi = mostPopularConcessionId)[0].nazwa
    u_procent = (liczba_biletow_u/(numberOfElectronicTickets+numberOfPaperTickets))*100
    u_procent = round(u_procent, 2)

    return render(request, template_name = "reportPage/ticketStats.html", context = 
    {'numberOfElectronicTickets': numberOfElectronicTickets, 'numberOfPaperTickets': numberOfPaperTickets,
    'mostPopularPaperTicket': mostPopularPaperTicket, 'liczba_biletow_k': liczba_biletow_k, 'mostPopularPaperTicketProcent': mostPopularPaperTicketProcent,
    'mostPopularConcession': mostPopularConcession, 'liczba_biletow_u': liczba_biletow_u, 
    'p_procent': p_procent, 'e_procent': e_procent, 'u_procent': u_procent,
    'mostPopularElectronicTicket': mostPopularElectronicTicket, 'liczba_biletow_e': liczba_biletow_e,
    'mostPopularElectronicTicketProcent': mostPopularElectronicTicketProcent})

def transactionPlaceStats(request):
    
    total_income_dictionary = Transakcje.objects.aggregate(Sum('kwota'))
    total_income = total_income_dictionary['kwota__sum']

    places = MiejscaTransakcji.objects.all()
    tmp=0;
    tmp_k=0
    max_income=0
    number_of_transactions=0; 
    most_popular_place_income=0   
    for place in places:
        transactions = Transakcje.objects.filter(id_miejsca_transakcji = place.id_miejsca_transakcji)
        tmp = transactions.count()
        tmp_k=0
        for transaction in transactions:
            tmp_k += transaction.kwota
        if tmp_k > max_income:
            max_income = tmp_k
            maxIncomePlaceId = place.id_miejsca_transakcji
        if tmp > number_of_transactions:
            number_of_transactions = tmp
            most_popular_place_income=tmp_k   
            mostPopularTransactionPlaceId = place.id_miejsca_transakcji
    
    max_income_procent = (max_income/(total_income))*100
    max_income_procent = round(max_income_procent, 2)

    most_popular_place_income_procent = (most_popular_place_income/(total_income))*100
    most_popular_place_income_procent = round(most_popular_place_income_procent, 2)

    mostPopularTransactionPlace = MiejscaTransakcji.objects.filter(id_miejsca_transakcji = mostPopularTransactionPlaceId)[0].nazwa
    maxIncomePlace = MiejscaTransakcji.objects.filter(id_miejsca_transakcji = maxIncomePlaceId)[0].nazwa
    most_popular_place_income = round(most_popular_place_income, 2)

    return render(request, template_name = "reportPage/transactionPlaceStats.html", context = 
    {'number_of_transactions': number_of_transactions, 'max_income': max_income, 'most_popular_place_income': most_popular_place_income,
    'mostPopularTransactionPlace': mostPopularTransactionPlace, 'maxIncomePlace': maxIncomePlace,
    'total_income': total_income, 'max_income_procent': max_income_procent, 
    'most_popular_place_income_procent': most_popular_place_income_procent})

def transactionStats(request):

    total_income_dictionary = Transakcje.objects.aggregate(Sum('kwota'))
    total_income = total_income_dictionary['kwota__sum']

    number_of_transactions = Transakcje.objects.all().count()

    average_income_of_transaction = total_income/number_of_transactions
    average_income_of_transaction = round(average_income_of_transaction, 2)

    transactions = Transakcje.objects.all()
    payments = MetodyPlatnosci.objects.all()
    tmp_t=0
    liczba_transakcji_m=0
    for payment in payments:
        tmp_t = Transakcje.objects.filter(id_metody_platnosci = payment.id_metody_platnosci).count()
        if tmp_t > liczba_transakcji_m:
            liczba_transakcji_m = tmp_t
            mostPopularPaymentMethodId = payment.id_metody_platnosci

    mostPopularPaymentMethod = MetodyPlatnosci.objects.filter(id_metody_platnosci = mostPopularPaymentMethodId)[0].nazwa
    
    return render(request, template_name = "reportPage/transactionStats.html", context = 
    {'total_income': total_income, 'number_of_transactions': number_of_transactions,
    'average_income_of_transaction': average_income_of_transaction,
    'mostPopularPaymentMethod': mostPopularPaymentMethod})

