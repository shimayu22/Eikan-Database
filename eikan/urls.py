from django.urls import path
from . import views

urlpatterns = [
    # /eikan/
    path('', views.IndexView.as_view(), name='index'),
    # チーム一覧 /eikan/team/
    path('team', views.TeamView.as_view(), name='teams'),
    # チーム詳細 /eikan/team/id/
    path('team/<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    # 選手一覧 /eikan/player/
    path('player', views.PlayerView.as_view(), name='player'),
    # 選手詳細 /eikan/player/id
    path('player/<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
]