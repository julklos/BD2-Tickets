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
    path('confirmCarton/<str:type>/<str:red>', views.confirmCarton, name="confirmCarton"),
    path('transactionCarton', views.transactionCarton, name= 'transactionCarton'),
    path('amount', views.amount, name="amount"),
    path('continueCarton', views.continueCarton, name="continueCarton"),
    path('zonesCard', views.selectZoneTicket, name="zonesCard"),
    path('thankyou', views.thankYou, name="thankyou")
    #path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
