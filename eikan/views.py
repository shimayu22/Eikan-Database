from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Teams, Players, TeamsTotalResults, \
                    FielderTotalResults, PitcherTotalResults

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'eikan/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['team_total_result'] = TeamsTotalResults.objects.latest('pk')
        start_year = (ctx['team_total_result'].year - 2) if ctx['team_total_result'].period == 1 else (ctx['team_total_result'].year - 1)
        players = Players.objects.filter(admission_year__gte=start_year, admission_year__lte=ctx['team_total_result'].year)
        pitchers = Players.objects.filter(admission_year__gte=start_year, admission_year__lte=ctx['team_total_result'].year, is_pitcher=True)
        ctx['fielder_total_results'] = FielderTotalResults.objects.filter(player_id__in=players).order_by('-ops', '-slg','player_id')
        ctx['pitcher_total_results'] = PitcherTotalResults.objects.filter(player_id__in=pitchers).order_by('player_id')

        return ctx

class TeamView(generic.ListView):
    template_name = 'eikan/team.html'
    context_object_name = 'team_list'

    def get_queryset(self):
        return Teams.objects.order_by('-year', '-period')
        #return TeamsTotalResults.order_by('team_id')

class TeamDetailView(generic.DetailView):
    model = Teams
    template_name = 'eikan/team_detail.html'

class PlayerView(generic.ListView):
    template_name = 'eikan/player.html'
    context_object_name = 'player_list'

    def get_queryset(self):
        return Players.objects.order_by('-admission_year','position')

class PlayerDetailView(generic.DetailView):
    model = Players
    template_name = 'eikan/player_detail.html'