from django.shortcuts import get_list_or_404, render
from django.urls import reverse
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
        ctx['teams'] = Teams.objects.latest('pk')
        ctx['team_total_result'] = TeamTotalResults.objects.get(
            team_id=ctx['teams'].pk)
        start_year = (
            ctx['teams'].year - 2) if ctx['teams'].period == 1 else (
            ctx['teams'].year - 1)
        players = Players.objects.filter(
            admission_year__gte=start_year,
            admission_year__lte=ctx['teams'].year)
        pitchers = Players.objects.filter(
            admission_year__gte=start_year,
            admission_year__lte=ctx['teams'].year,
            is_pitcher=True)
        ctx['fielder_total_results'] = FielderTotalResults.objects.filter(
            player_id__in=players).order_by('-ops', '-slg', 'player_id')
        ctx['pitcher_total_results'] = PitcherTotalResults.objects.filter(
            player_id__in=pitchers).order_by('player_id')

        return ctx


class TeamView(ListView):
    model = TeamTotalResults
    template_name = 'eikan/teams.html'
    context_object_name = 'team_total_results'


class TeamDetailView(DetailView):
    model = Teams
    template_name = 'eikan/team_detail.html'


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
                if f.exists():
                    sfs = s.PitcherSabrManager(player, p)
                    ctx[key] = sfs.create_sabr_from_results()

        return ctx
