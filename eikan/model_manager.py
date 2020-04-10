class DefaultValueExtractor:
    @staticmethod
    def create_default_year_for_teams():
        from eikan.models import Teams
        if not Teams.objects.exists():
            return 1941

        period = Teams.objects.latest('pk').period
        this_year = Teams.objects.latest('pk').year
        return this_year if period == 1 else this_year + 1

    @staticmethod
    def create_default_period():
        from eikan.models import Teams
        if not Teams.objects.exists():
            return 1

        return 1 if Teams.objects.latest('pk').period == 2 else 2

    @staticmethod
    def create_default_prefecture():
        from eikan.models import Teams
        return 0 if not Teams.objects.exists() else Teams.objects.latest('pk').prefecture

    @staticmethod
    def create_default_year_for_players():
        from eikan.models import Teams
        return Teams.objects.latest(
            'pk').year if Teams.objects.exists() else 1939

    @staticmethod
    def create_default_team_id():
        from eikan.models import Teams
        return Teams.objects.latest('pk').id if Teams.objects.exists() else 0

    @staticmethod
    def create_default_team_rank():
        from eikan.models import Games
        return Games.objects.latest('pk').rank if Games.objects.exists() else 0

    @staticmethod
    def select_display_players():
        from eikan.models import Teams, ModelSettings

        if ModelSettings.objects.exists() and ModelSettings.objects.latest(
                'pk').is_used_limit_choices_to:
            return {}

        if not Teams.objects.exists():
            return {}

        teams = Teams.objects.latest('pk')
        if teams.period == 1:
            return {
                "admission_year__gte": teams.year - 2,
                "admission_year__lte": teams.year}
        else:
            return {
                "admission_year__gte": teams.year - 1,
                "admission_year__lte": teams.year}

    @staticmethod
    def select_display_pitchers():
        from eikan.models import Teams, ModelSettings

        if ModelSettings.objects.exists() and ModelSettings.objects.latest(
                'pk').is_used_limit_choices_to:
            return {"is_pitcher": True}

        if not Teams.objects.exists():
            return {"is_pitcher": True}

        teams = Teams.objects.latest('pk')
        if teams.period == 1:
            return {
                "is_pitcher": True,
                "admission_year__gte": teams.year - 2,
                "admission_year__lte": teams.year}
        else:
            return {
                "is_pitcher": True,
                "admission_year__gte": teams.year - 1,
                "admission_year__lte": teams.year}


class SavedValueExtractor:
    def create_game_results(self, score, run):
        return 1 if score > run else 2 if score < run else 3

    def update_is_pitcher(self, position, is_pitched):
        return position == 1 or is_pitched
