from django.shortcuts import get_list_or_404
from django.views.generic import TemplateView, ListView, DetailView
from eikan import sabr_manager as s

from .models import Teams, Players, Games, \
    FielderResults, PitcherResults, \
    FielderTotalResults, PitcherTotalResults, TeamTotalResults

# Create your views here.


class IndexView(TemplateView):
    template_name = 'eikan/index.html'

    def get_context_data(self, **kwargs):
        # 雑な404
        get_list_or_404(Teams)
        get_list_or_404(Players)

        ctx = super().get_context_data(**kwargs)
        # ctx['teams'] = Teams.objects.latest('pk')
        ctx['team_total_result'] = TeamTotalResults.objects.select_related('team_id').latest('pk')
        start_year = (
            ctx['team_total_result'].team_id.year - 2) if ctx['team_total_result'].team_id.period == 1 else (
            ctx['team_total_result'].team_id.year - 1)
        players = Players.objects.filter(
            admission_year__gte=start_year,
            admission_year__lte=ctx['team_total_result'].team_id.year)
        pitchers = Players.objects.filter(
            admission_year__gte=start_year,
            admission_year__lte=ctx['team_total_result'].team_id.year,
            is_pitcher=True)
        ctx['fielder_total_results'] = FielderTotalResults.objects.select_related('player_id').filter(
            player_id__in=players).order_by('-ops', '-slg', 'player_id')
        ctx['pitcher_total_results'] = PitcherTotalResults.objects.select_related('player_id').filter(
            player_id__in=pitchers).order_by('player_id')

        return ctx


class TeamView(ListView):
    model = TeamTotalResults
    template_name = 'eikan/teams.html'
    context_object_name = 'team_total_results'


class TeamDetailView(DetailView):
    model = Teams
    template_name = 'eikan/team_detail.html'

    def get_context_data(self, **kwargs):
        teams = kwargs['object']

        ctx = super().get_context_data(**kwargs)
        ctx['games'] = Games.objects.select_related('team_id').filter(team_id=teams).order_by('-pk')
        # このチームで行った試合結果を取得する
        ctx['fielder_results'] = []
        # 取得したい選手のリストを作る
        fielder_results = FielderResults.objects.select_related('player_id').filter(
            game_id__team_id=teams).order_by('player_id')
        player_list = fielder_results.values('player_id').distinct()
        # <QuerySet [{'player_id': 1}, {'player_id': 2}, {'player_id': 3}, {'player_id': 4}]>
        # 選手ごとにこのチームだった時の指標を計算する
        if fielder_results.exists():
            for f in player_list:
                sfs = s.FielderSabrManager(
                    f['player_id'], fielder_results.filter(
                        player_id=f['player_id']))
                ctx['fielder_results'].append(sfs.create_sabr_from_results())

        # 投手編
        ctx['pitcher_results'] = []
        pitcher_results = PitcherResults.objects.select_related('player_id').filter(
            game_id__team_id=teams).order_by('player_id')
        pitcher_list = pitcher_results.values('player_id').distinct()
        if pitcher_results.exists():
            for p in pitcher_list:
                sfs = s.PitcherSabrManager(
                    p['player_id'], pitcher_results.filter(
                        player_id=p['player_id']))
                ctx['pitcher_results'].append(sfs.create_sabr_from_results())

        return ctx


class FielderView(ListView):
    model = FielderTotalResults
    template_name = 'eikan/fielders.html'
    context_object_name = 'fielder_total_results'


class PitcherView(ListView):
    model = PitcherTotalResults
    template_name = 'eikan/pitchers.html'
    context_object_name = 'pitcher_total_results'


class PlayerDetailView(DetailView):
    model = Players
    template_name = 'eikan/player_detail.html'

    def get_context_data(self, **kwargs):
        player = kwargs['object']

        ctx = super().get_context_data(**kwargs)
        # 打者総合成績を取得（投手野手共通）
        fielder_total_results = FielderTotalResults.objects.get(
            player_id=player)
        ctx['fielder_total_results'] = fielder_total_results
        # 1年生時の西暦から、3年夏までの試合結果を取得する
        fielder_results = FielderResults.objects.filter(
            player_id=player)
        ctx['fielder_results'] = fielder_results
        # ctx["fielder_results_n"] n=1～3
        for i in range(0, 3):
            key = "fielder_results_" + str(i + 1)
            ctx[key] = []
            year = player.admission_year + i
            f = fielder_results.filter(game_id__team_id__year=year)
            if f.exists():
                sfs = s.FielderSabrManager(player, f)
                ctx[key] = sfs.create_sabr_from_results()

        # 投手のみ以下の処理を行う
        if player.is_pitcher:
            pitcher_total_results = PitcherTotalResults.objects.get(
                player_id=player)
            ctx['pitcher_total_results'] = pitcher_total_results
            pitcher_results = PitcherResults.objects.filter(
                player_id=player)
            ctx['pitcher_results'] = pitcher_results
            for i in range(0, 3):
                key = "pitcher_results_" + str(i + 1)
                ctx[key] = []
                year = player.admission_year + i
                p = pitcher_results.filter(game_id__team_id__year=year)
                if p.exists():
                    sfs = s.PitcherSabrManager(player, p)
                    ctx[key] = sfs.create_sabr_from_results()

        return ctx


class GameView(ListView):
    model = Games
    template_name = 'eikan/games.html'
    context_object_name = 'games'


class GameDetailView(DetailView):
    model = Games
    template_name = 'eikan/game_detail.html'

    def get_context_data(self, **kwargs):
        game = kwargs['object']

        ctx = super().get_context_data(**kwargs)
        ctx['fielder_results'] = FielderResults.objects.filter(
            game_id=game).order_by('pk')
        ctx['pitcher_results'] = PitcherResults.objects.filter(
            game_id=game).order_by('pk')

        return ctx
