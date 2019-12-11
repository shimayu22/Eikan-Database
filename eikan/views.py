from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Teams, Players ,TeamsTotalResults ,FielderTotalResults

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'eikan/index.html'
    context_object_name = 'team_list'

    def get_queryset(self):
        return Teams.objects.order_by('-year', '-period')[:3]
        #return TeamsTotalResults.order_by('team_id')[:3]

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