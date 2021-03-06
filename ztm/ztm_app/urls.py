from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'ztm_app'

urlpatterns = [
    # path("teams", views.TeamListView.as_view(), name="team_list"),
    # path("teams/<str:version>/<str:pk>", views.TeamDetailView.as_view(), name="team_detail"),
    # path("teams/add", views.TeamCreateView.as_view(), name="team_add"),
    # path("teams/update/<str:version>/<str:pk>", views.TeamUpdateView.as_view(), name="team_update"),
    path('index', views.index, name="index"),
    path('card', views.selectCard, name='card'),
    path('zones', views.zonesCarton, name='zonesCarton'),
    path('timeCarton/<str:zone>', views.timeCarton, name='timeCarton'),
    path('selectTicketCarton', views.selectTicketCarton, name= 'selectTicketCarton' ),
    path('reductionCarton', views.reductionCarton, name='reductionCarton'),
    path('confirmCarton', views.confirmCarton, name="confirmCarton"),
    path('transactionCarton', views.transactionCarton, name= 'transactionCarton'),
    path('transactionCard', views.transactionCard, name= 'transactionCard'),
    path('amount', views.amount, name="amount"),
    path('continueCarton', views.continueCarton, name="continueCarton"),
    path('zonesCard', views.selectZoneTicket, name="zonesCard"),
    path('thankyou', views.thankYou, name="thankyou"),
    path('confirmCard', views.confirmCard, name="confirmCard"),
    path('selectTicket', views.selectTicket, name="selectTicket"),
    path('findTicket', views.findTicket, name = "findTicket"),
    path('transactionActivation', views.transactionActivation, name= "transactionActivation"),
    path('end', views.end, name= "end"),
    path('reportPage', views.reportPage, name="reportPage"),
    path('editPage', views.editPage, name="editPage"),
    path('statsPage', views.statsPage, name="statsPage"),
    path('addConcession', views.addConcession, name="addConcession"),
    path('addCardType', views.addCardType, name="addCardType"),
    path('deleteConcession', views.deleteConcession, name="deleteConcession"),    
    path('deleteCardType', views.deleteCardType, name="deleteCardType"),
    path('updateCardType', views.updateCardType, name="updateCardType"),
    path('updateConcession', views.updateConcession, name="updateConcession"),
    path('ticketStats', views.ticketStats, name="ticketStats"),
    path('transactionPlaceStats', views.transactionPlaceStats, name="transactionPlaceStats"),
    path('transactionStats', views.transactionStats, name="transactionStats"),
    #path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
