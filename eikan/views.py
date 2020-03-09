from django.shortcuts import get_list_or_404
from django.views.generic import TemplateView, DetailView, ListView
from eikan import fielder_sabr_manager as f
from eikan import pitcher_sabr_manager as p

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


class TeamView(ListView):
    template_name = 'eikan/teams.html'
    queryset = TeamTotalResults.objects.select_related(
        'team_id').all().order_by('team_id')
    context_object_name = 'team_total_results'
    paginate_by = 100


class TeamDetailView(DetailView):
    model = Teams
    template_name = 'eikan/team_detail.html'

    def get_context_data(self, **kwargs):
        teams = kwargs['object']

        ctx = super().get_context_data(**kwargs)
        ctx['team_total_result'] = TeamTotalResults.objects.select_related(
            'team_id').get(team_id=teams)
        ctx['games'] = Games.objects.select_related(
            'team_id').filter(team_id=teams).order_by('-pk')
        g = Games.objects.select_related(
            'team_id').filter(team_id=teams, competition_type__gt=1)
        if g.exists():
            ctx['game_latest'] = g.latest('pk')
        # このチームで行った試合結果を取得する
        ctx['fielder_results'] = f.FielderSabrFormatter(
        ).create_sabr_from_results_of_team(teams)
        # 投手編
        ctx['pitcher_results'] = p.PitcherSabrFormatter(
        ).create_sabr_from_results_of_team(teams)

        return ctx


class FielderView(ListView):
    template_name = 'eikan/fielders.html'
    queryset = FielderTotalResults.objects.select_related(
        'player_id').all().order_by('-player_id')
    context_object_name = 'fielder_total_results'
    paginate_by = 100


class PitcherView(ListView):
    template_name = 'eikan/pitchers.html'
    queryset = PitcherTotalResults.objects.select_related(
        'player_id').all().order_by('-player_id')
    context_object_name = 'pitcher_total_results'
    paginate_by = 100


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
            'game_id__team_id', 'game_id', 'player_id').filter(
            player_id=player).order_by('-pk')
        ctx['fielder_by_year_results'] = f.FielderSabrFormatter(
        ).create_sabr_from_results_by_year(player)

        # 投手のみ以下の処理を行う
        if player.is_pitcher:
            ctx['pitcher_total_results'] = PitcherTotalResults.objects.select_related(
                'player_id').get(player_id=player)
            ctx['pitcher_results'] = PitcherResults.objects.select_related(
                'game_id__team_id', 'game_id', 'player_id').filter(
                player_id=player).order_by('-pk')
            ctx['pitcher_by_year_results'] = p.PitcherSabrFormatter(
            ).create_sabr_from_results_by_year(player)

        return ctx


class GameView(ListView):
    template_name = 'eikan/games.html'
    queryset = Games.objects.select_related(
        'team_id').all().order_by('-pk')
    context_object_name = 'games'
    paginate_by = 100


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
