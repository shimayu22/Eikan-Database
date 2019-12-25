from django.shortcuts import get_list_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView

from .models import Teams, Players, TeamTotalResults, \
                    FielderTotalResults, PitcherTotalResults

# Create your views here.
class IndexView(TemplateView):
    template_name = 'eikan/index.html'

    def get_context_data(self, **kwargs):
        # 雑な404
        get_list_or_404(Teams)
        get_list_or_404(Players)

        ctx = super().get_context_data(**kwargs)
        ctx['teams'] = Teams.objects.latest('pk')
        ctx['team_total_result'] = TeamTotalResults.objects.get(team_id=ctx['teams'].pk)
        start_year = (ctx['teams'].year - 2) if ctx['teams'].period == 1 else (ctx['teams'].year - 1)
        players = Players.objects.filter(admission_year__gte=start_year, admission_year__lte=ctx['teams'].year)
        pitchers = Players.objects.filter(admission_year__gte=start_year, admission_year__lte=ctx['teams'].year, is_pitcher=True)
        ctx['fielder_total_results'] = FielderTotalResults.objects.filter(player_id__in=players).order_by('-ops', '-slg')
        ctx['pitcher_total_results'] = PitcherTotalResults.objects.filter(player_id__in=pitchers)

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
        player_id = kwargs['object']
        
        ctx = super().get_context_data(**kwargs)
        ctx['fielder_total_results'] = FielderTotalResults.objects.get(player_id=player_id)
        if player_id.is_pitcher:
            ctx['pitcher_total_results'] = PitcherTotalResults.objects.get(player_id=player_id)
        
        return ctx