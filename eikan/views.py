from django.shortcuts import get_list_or_404
from django.views.generic import TemplateView, DetailView
from eikan import sabr_manager as s
from eikan import sabr_manager_for_player as p

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
        ctx['team_total_result'] = TeamTotalResults.objects.select_related(
            'team_id').latest('pk')
        start_year = (
            ctx['team_total_result'].team_id.year -
            2) if ctx['team_total_result'].team_id.period == 1 else (
            ctx['team_total_result'].team_id.year -
            1)
        players = Players.objects.filter(
            admission_year__gte=start_year,
            admission_year__lte=ctx['team_total_result'].team_id.year)
        pitchers = Players.objects.filter(
            admission_year__gte=start_year,
            admission_year__lte=ctx['team_total_result'].team_id.year,
            is_pitcher=True)
        ctx['fielder_total_results'] = FielderTotalResults.objects.select_related(
            'player_id').filter(player_id__in=players).order_by('-ops', '-slg', 'player_id')
        ctx['pitcher_total_results'] = PitcherTotalResults.objects.select_related(
            'player_id').filter(player_id__in=pitchers).order_by('player_id')

        return ctx


class TeamView(TemplateView):
    template_name = 'eikan/teams.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['team_total_results'] = TeamTotalResults.objects.select_related(
            'team_id').all().order_by('team_id')

        return ctx


class TeamDetailView(DetailView):
    model = Teams
    template_name = 'eikan/team_detail.html'

    def get_context_data(self, **kwargs):
        teams = kwargs['object']

        ctx = super().get_context_data(**kwargs)
        ctx['games'] = Games.objects.select_related(
            'team_id').filter(team_id=teams).order_by('-pk')
        # このチームで行った試合結果を取得する
        ctx['fielder_results'] = []
        # 取得したい選手のリストを作る
        fielder_results = FielderResults.objects.select_related(
            'player_id').filter(game_id__team_id=teams).order_by('player_id')

        player_list = fielder_results.values('player_id').distinct()
        # <QuerySet [{'player_id': 1}, {'player_id': 2}, {'player_id': 3}, {'player_id': 4}]>
        # 選手ごとにこのチームだった時の指標を計算する
        for f in player_list:
            sfs = s.FielderSabrManager(
                f['player_id'], fielder_results.filter(
                    player_id=f['player_id']))
            ctx['fielder_results'].append(sfs.create_sabr_from_results())

        # 投手編
        ctx['pitcher_results'] = []
        pitcher_results = PitcherResults.objects.select_related(
            'player_id').filter(game_id__team_id=teams).order_by('player_id')
        pitcher_list = pitcher_results.values('player_id').distinct()
        for p in pitcher_list:
            sfs = s.PitcherSabrManager(
                p['player_id'], pitcher_results.filter(
                    player_id=p['player_id']))
            ctx['pitcher_results'].append(sfs.create_sabr_from_results())

        return ctx


class FielderView(TemplateView):
    template_name = 'eikan/fielders.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['fielder_total_results'] = FielderTotalResults.objects.select_related(
            'player_id').all().order_by('player_id')

        return ctx


class PitcherView(TemplateView):
    template_name = 'eikan/pitchers.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pitcher_total_results'] = PitcherTotalResults.objects.select_related(
            'player_id').all().order_by('player_id')

        return ctx


class PlayerDetailView(DetailView):
    model = Players
    template_name = 'eikan/player_detail.html'

    def get_context_data(self, **kwargs):
        player = kwargs['object']

        ctx = super().get_context_data(**kwargs)
        # 打者総合成績を取得（投手野手共通）
        ctx['fielder_total_results'] = FielderTotalResults.objects.select_related(
            'player_id').get(player_id=player)
        # 1年生時の西暦から、3年夏までの試合結果を取得する
        ctx['fielder_results'] = FielderResults.objects.select_related(
            'game_id__team_id', 'game_id', 'player_id').filter(player_id=player)
        pfs = p.FielderByYearSabrManager(player)
        ctx['fielder_by_year_results'] = pfs.create_sabr_from_results()

        # 投手のみ以下の処理を行う
        if player.is_pitcher:
            ctx['pitcher_total_results'] = PitcherTotalResults.objects.select_related(
                'player_id').get(player_id=player)
            ctx['pitcher_results'] = PitcherResults.objects.select_related(
                'game_id__team_id', 'game_id', 'player_id').filter(player_id=player)
            pps = p.PitcherByYearSabrManager(player)
            ctx['pitcher_by_year_results'] = pps.create_sabr_from_results()

        return ctx


class GameView(TemplateView):
    template_name = 'eikan/games.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['games'] = Games.objects.select_related(
            'team_id').all().order_by('team_id')

        return ctx


class GameDetailView(DetailView):
    model = Games
    template_name = 'eikan/game_detail.html'

    def get_context_data(self, **kwargs):
        game = kwargs['object']

        ctx = super().get_context_data(**kwargs)
        ctx['fielder_results'] = FielderResults.objects.select_related(
            'player_id').filter(game_id=game).order_by('pk')
        ctx['pitcher_results'] = PitcherResults.objects.select_related(
            'player_id').filter(game_id=game).order_by('pk')

        return ctx
