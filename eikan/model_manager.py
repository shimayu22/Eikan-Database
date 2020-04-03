class DefaultValueExtractor:
    pass


class SavedValueExtractor:
    def create_game_results(self, score, run):
        if score == run:
            return 3

        return 1 if score > run else 2

    def update_is_pitcher(self, position, is_pitched):
        return position == 1 or is_pitched
