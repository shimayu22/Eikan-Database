from django.shortcuts import get_list_or_404, redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.urls import reverse
from eikan import fielder_sabr_manager as f
from eikan import pitcher_sabr_manager as p
from eikan import team_sabr_manager as t
from eikan.model_manager import ChoicesFormatter as c
from datetime import datetime, timezone, timedelta
from .models import Teams, Players, Games, \
    FielderResults, PitcherResults, \
    FielderTotalResults, PitcherTotalResults, TeamTotalResults


def update_total_results(request, pk=None):
    """TeamTotalResultsの更新

    Args:
        request
        pk (int, optional): TeamsのPK. Defaults to None.

    Returns:
        indexまたは表示しているチーム詳細画面にリダイレクトする

    Notes:
        pkない場合はindexからの更新、あればチーム詳細からの更新
    """
    if not Teams.objects.exists():
        return redirect('eikan:index')

    team_id = Teams.objects.latest('pk')
    redirect_url = reverse('eikan:index')
    url = redirect_url

    # pkがある=チーム詳細からの更新、ない=indexからの更新
    if pk and Teams.objects.filter(pk=pk).exists():
        team_id = Teams.objects.get(pk=pk)
        redirect_url = reverse('eikan:teams')
        url = f'{redirect_url}/{str(pk)}/'

    # 連打されてもいいように
    if TeamTotalResults.objects.get(
            team=team_id).updated_at + timedelta(minutes=1) < datetime.now(timezone.utc):
        t.TeamSabrFormatter().update_total_results(team_id)

    return redirect(url)


def update_all_players_total_results(request):
    """登録されている全ての選手を再計算する

    Args:
        request

    Returns:
        indexにリダイレクトする

    Notes:
        打者→投手→チーム総合成績を計算し直してDBに登録する
    """
    if not Players.objects.exists():
        return redirect('eikan:index')

    # 打者総合成績を更新
    f.FielderSabrFormatter().update_all_total_results()
    # 投手総合成績を更新
    p.PitcherSabrFormatter().update_all_total_results()
    # チーム総合成績を更新
    t.TeamSabrFormatter().update_all_total_results()

    return redirect('eikan:index')


class IndexView(TemplateView):
    """index：現在のチーム情報を表示する

    Notes:
        team_total_result: 現在のチーム情報。
        fielder_total_results: 現在のチームの打者総合成績。
        pitcher_total_results: 現在のチームの投手総合成績。
    """
    template_name = 'eikan/index.html'

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)
        # 現在のチームを取得
        if TeamTotalResults.objects.exists():
            ctx['team_total_result'] = TeamTotalResults.objects.select_related(
                'team').latest('pk')
        else:
            return ctx

        # 現在のチームの選手を取得
        start_year = (
            ctx['team_total_result'].team.year -
            2) if ctx['team_total_result'].team.period == 1 else (
            ctx['team_total_result'].team.year -
            1)
        players = Players.objects.filter(
            admission_year__gte=start_year,
            admission_year__lte=ctx['team_total_result'].team.year)
        pitchers = Players.objects.filter(
            admission_year__gte=start_year,
            admission_year__lte=ctx['team_total_result'].team.year,
            is_pitcher=True)
        ctx['fielder_total_results'] = FielderTotalResults.objects.select_related(
            'player').filter(player__in=players).order_by('-ops', '-slg', '-obp', 'player')
        ctx['pitcher_total_results'] = PitcherTotalResults.objects.select_related(
            'player').filter(player__in=pitchers).order_by('-innings_pitched', 'player')

        return ctx


class TeamView(ListView):
    """ チーム一覧を表示する """
    template_name = 'eikan/teams.html'
    queryset = TeamTotalResults.objects.select_related(
        'team').all().order_by('team')
    context_object_name = 'team_total_results'
    paginate_by = 100


class TeamDetailView(DetailView):
    """ チーム詳細を表示する

    Notes:
        team_total_result: チーム総合成績
        games: このチームで行われた試合一覧
        fielder_total_results: このチームで行われた試合の打者成績
        pitcher_total_results: このチームで行われた試合の投手成績
    """
    model = Teams
    template_name = 'eikan/team_detail.html'

    def get_context_data(self, **kwargs):
        teams = kwargs['object']

        ctx = super().get_context_data(**kwargs)
        ctx['team_total_result'] = TeamTotalResults.objects.select_related(
            'team').get(team=teams)
        ctx['games'] = Games.objects.select_related(
            'team_id').filter(team_id=teams).order_by('-pk')
        competition_choices = c.competition_choices_to_dict()
        g = Games.objects.select_related('team_id').filter(
            team_id=teams, competition_type__gt=competition_choices['練習試合'])
        if g.exists():
            ctx['game_latest'] = g.latest('pk')
        # このチームで行った試合結果を取得する
        ctx['fielder_total_results'] = f.FielderSabrFormatter(
        ).create_sabr_from_results_of_team(teams)
        # 投手編
        ctx['pitcher_total_results'] = p.PitcherSabrFormatter(
        ).create_sabr_from_results_of_team(teams)

        return ctx


class FielderView(ListView):
    """ 打者成績一覧

    Notes:
        選手詳細画面は投手と共通
    """
    template_name = 'eikan/fielders.html'
    queryset = FielderTotalResults.objects.select_related(
        'player').all().order_by('-player')
    context_object_name = 'fielder_total_results'
    paginate_by = 100


class PitcherView(ListView):
    """ 投手成績一覧

    Notes:
        選手詳細画面は打者と共通
    """
    template_name = 'eikan/pitchers.html'
    queryset = PitcherTotalResults.objects.select_related(
        'player').all().order_by('-player')
    context_object_name = 'pitcher_total_results'
    paginate_by = 100


class PlayerDetailView(DetailView):
    """選手詳細を表示する

    Notes:
        fielder_total_results: 打者総合成績（以下投手野手共通）
        fielder_results: 1年夏から3年夏までの試合結果
        fielder_by_year_results: 学年ごとに集計した打者総合成績
        pitcher_total_results: 投手総合成績（以下投手のみ取得）
        pitcher_results: 1年夏から3年夏までの試合結果
        pitcher_by_year_results: 学年ごとに集計した投手総合成績
    """
    model = Players
    template_name = 'eikan/player_detail.html'

    def get_context_data(self, **kwargs):
        player = kwargs['object']
        ctx = super().get_context_data(**kwargs)
        # 打者総合成績を取得（投手野手共通）
        ctx['fielder_total_results'] = FielderTotalResults.objects.select_related(
            'player').get(player=player)
        # 1年生時の西暦から、3年夏までの試合結果を取得する
        ctx['fielder_results'] = FielderResults.objects.select_related(
            'game_id__team_id', 'game_id', 'player_id').filter(
            player_id=player).order_by('-pk')
        ctx['fielder_by_year_results'] = f.FielderSabrFormatter(
        ).create_sabr_from_results_by_year(player)

        # 投手のみ以下の処理を行う
        if player.is_pitcher:
            ctx['pitcher_total_results'] = PitcherTotalResults.objects.select_related(
                'player').get(player=player)
            ctx['pitcher_results'] = PitcherResults.objects.select_related(
                'game_id__team_id', 'game_id', 'player_id').filter(
                player_id=player).order_by('-pk')
            ctx['pitcher_by_year_results'] = p.PitcherSabrFormatter(
            ).create_sabr_from_results_by_year(player)

        return ctx


class GameView(ListView):
    """ 試合一覧 """
    template_name = 'eikan/games.html'
    queryset = Games.objects.select_related(
        'team_id').all().order_by('-pk')
    context_object_name = 'games'
    paginate_by = 100


class GameDetailView(DetailView):
    """試合詳細を表示する

    Notes:
        game: 試合結果
        fielder_results: その試合の打撃結果
        pitcher_results: その試合の投球結果
    """
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
