from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'ztm_app'

urlpatterns = [
    # path("teams", views.TeamListView.as_view(), name="team_list"),
    # path("teams/<str:version>/<str:pk>", views.TeamDetailView.as_view(), name="team_detail"),
    # path("teams/add", views.TeamCreateView.as_view(), name="team_add"),
    # path("teams/update/<str:version>/<str:pk>", views.TeamUpdateView.as_view(), name="team_update"),
    url('index', views.index, name="index"),
    url('card', views.card, name='card'),
    url('carton', views.carton, name='carton'),
    #path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
