from django.urls import path
from . import views

app_name = 'eikan'
urlpatterns = [
    # /eikan/
    path('', views.IndexView.as_view(), name='index'),
    # チーム一覧 /eikan/team
    path('teams', views.TeamView.as_view(), name='teams'),
    # チーム詳細 /eikan/team/id/
    path(
        'teams/<int:pk>/',
        views.TeamDetailView.as_view(),
        name='team_detail'),
    # 野手（成績）一覧 /eikan/fielders
    path('fielders', views.FielderView.as_view(), name='fielders'),
    # 投手（成績）一覧 /eikan/pitchers
    path('pitchers', views.PitcherView.as_view(), name='pitchers'),
    # 選手詳細 /eikan/player/id
    # 投手、野手のリンクからどちらもここに遷移する
    path(
        'players/<int:pk>/',
        views.PlayerDetailView.as_view(),
        name='player_detail'),
]
