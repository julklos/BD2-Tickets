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
    path('card', views.selectCard, name='selectCard'),
    path('zones', views.zonesCarton, name='zonesCarton'),
    path('timeCarton/<str:zone>', views.timeCarton, name='timeCarton'),
    path('reductionCarton', views.reductionCarton, name='reductionCarton'),
    path('confirmCarton', views.confirmCarton, name="confirmCarton"),
    path('zonesCard', views.selectZoneTicket, name="zonesCard")
    #path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
