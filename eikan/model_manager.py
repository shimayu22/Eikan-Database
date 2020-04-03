class DefaultValueExtractor:
    @classmethod
    def create_default_year_for_teams(self):
        from eikan.models import Teams
        if not Teams.objects.exists():
            return 1941

        period = Teams.objects.latest('pk').period
        this_year = Teams.objects.latest('pk').year
        return this_year if period == 1 else this_year + 1
    
    @classmethod
    def create_default_period(self):
        from eikan.models import Teams
        if not Teams.objects.exists():
            return 1
        
        return 1 if Teams.objects.latest('pk').period == 2 else 2
    
    @classmethod
    def create_default_prefecture(self):
        from eikan.models import Teams
        return 0 if not Teams.objects.exists() else Teams.objects.latest('pk').prefecture


class SavedValueExtractor:
    def create_game_results(self, score, run):
        return 1 if score > run else 2 if score < run else 3

    def update_is_pitcher(self, position, is_pitched):
        return position == 1 or is_pitched
