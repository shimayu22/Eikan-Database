from django.urls import path
from . import views

app_name = 'eikan'
urlpatterns = [
    # 表示用
    # /eikan/
    path('', views.IndexView.as_view(), name='index'),
    # チーム一覧 /eikan/teams
    path('teams', views.TeamView.as_view(), name='teams'),
    # チーム詳細 /eikan/teams/id/
    path(
        'teams/<int:pk>/',
        views.TeamDetailView.as_view(),
        name='team_detail'),
    # 野手（成績）一覧 /eikan/fielders
    path('fielders', views.FielderView.as_view(), name='fielders'),
    # 投手（成績）一覧 /eikan/pitchers
    path('pitchers', views.PitcherView.as_view(), name='pitchers'),
    # 選手詳細 /eikan/players/id
    # 投手、野手のリンクからどちらもここに遷移する
    path(
        'players/<int:pk>/',
        views.PlayerDetailView.as_view(),
        name='player_detail'),
    # 試合一覧 /eikan/games
    path('games', views.GameView.as_view(), name='games'),
    # 試合詳細 /eikan/games/id
    path(
        'games/<int:pk>/',
        views.GameDetailView.as_view(),
        name='game_detail'),

    # データ更新用
    # 現在のページに表示されているチームを更新する
    path('update', views.update_total_results, name='update'),
]
