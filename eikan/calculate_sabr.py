from django.db import models
from eikan.models import Teams, Players, Games, Fielder_results, Pitcher_results

class CalculateSabr:
    def __init__(self,game_id,player_id):
        self.game_id = game_id
        self.player_id = player_id

    def total_bases(self):
        return Fielder_results.objects.filter(player_id=2).aggregate(models.Sum('hit'))