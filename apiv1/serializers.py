from rest_framework import serializers
from eikan.models import Games


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = (
            'id',
            'team_id',
            'competition_type',
            'competition_round',
            'result',
            'score',
            'run',
            'is_cold_game',
            'mamono_count',
            'rank',
        )
