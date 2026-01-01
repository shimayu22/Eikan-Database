from django.test import TestCase
from eikan.models import Teams, Games, ModelSettings
from eikan import defaults
from eikan.model_manager import SavedValueExtractor, ChoicesFormatter


class DefaultValueExtractorTests(TestCase):
    def test_create_default_year_for_teams(self):
        """
        Teamsにレコードが存在しない場合 -> 1941(初期値)
        Teamsにレコードが存在して、最新レコードが
            period == 1(夏) -> 同じyearを返す
            period == 2(秋) -> 次のyearを返す
        """
        self.assertEqual(
            defaults.create_default_year_for_teams(), 1941)
        Teams(year=1985, period=1).save()
        self.assertEqual(
            defaults.create_default_year_for_teams(), 1985)
        Teams(year=1985, period=2).save()
        self.assertEqual(
            defaults.create_default_year_for_teams(), 1986)

    def test_create_default_period(self):
        """
        Teamsにレコードが存在しない場合 -> 1(夏:初期値)
        Teamsにレコードが存在して、最新レコードが
            period == 1(夏) -> 2(秋)を返す
            period == 2(秋) -> 1(夏)を返す
        """
        self.assertEqual(defaults.create_default_period(), 1)
        Teams(year=1985, period=1).save()
        self.assertEqual(defaults.create_default_period(), 2)
        Teams(year=1985, period=2).save()
        self.assertEqual(defaults.create_default_period(), 1)

    def test_create_default_prefecture(self):
        """
        Teamsにレコードが存在しない場合   -> 0(初期値)
        Teamsにレコードが存在している場合 -> 最新レコードのprefectureと同じ値を返す
        """
        self.assertEqual(defaults.create_default_prefecture(), 0)
        Teams(prefecture=17).save()
        self.assertEqual(defaults.create_default_prefecture(), 17)
        Teams(prefecture=1).save()
        self.assertEqual(defaults.create_default_prefecture(), 1)

    def test_create_default_year_for_players(self):
        """
        Teamsにレコードが存在しない場合   -> 1939(初期値)
        Teamsにレコードが存在している場合 -> 最新レコードのyearと同じ値を返す
        """
        self.assertEqual(
            defaults.create_default_year_for_players(), 1939)
        Teams(year=1985).save()
        self.assertEqual(
            defaults.create_default_year_for_players(), 1985)
        Teams(year=2040).save()
        self.assertEqual(
            defaults.create_default_year_for_players(), 2040)

    def test_create_default_team_id(self):
        """
        Teamsにレコードが存在しない場合   -> 1939(初期値)
        Teamsにレコードが存在している場合 -> 最新レコードのidと同じ値を返す
        """
        self.assertEqual(defaults.create_default_team_id(), '')
        Teams(year=1985, period=1).save()
        self.assertEqual(defaults.create_default_team_id(), 1)
        Teams(year=1985, period=2).save()
        self.assertEqual(defaults.create_default_team_id(), 2)

    def test_create_default_competition_type(self):
        """
        現在のチームに紐づくGamesのレコードが存在しない場合 -> 2(県大会)
        現在のそのチームに紐づくGamesのレコードが存在する場合
            最新が練習試合 -> 2(県大会)
            練習試合以外 -> 基本は同じ値を設定する
                例外:
                    夏 and 県大会 and 決勝 and 勝　であれば次は甲子園
                    秋 and 県大会 and ２回戦 and 勝　であれば次は地区大会
                    秋 and 地区大会 and ２回戦　であれば次はセンバツ
                妥協：
                    １回戦、３回戦がない場合は考慮しない
        """
        period = ChoicesFormatter.period_choices_to_dict()
        competition_choices = ChoicesFormatter.competition_choices_to_dict()
        round_choices = ChoicesFormatter.round_choices_to_dict()

        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])
        # 夏のチーム
        Teams(year=1985, period=period['夏']).save()

        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        t1 = Teams.objects.latest('pk')
        Games(
            team_id=t1,
            competition_type=competition_choices['練習試合'],
            competition_round=round_choices['練習試合']
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['甲子園'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['決勝'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        # 甲子園進出後のテスト（夏のチーム）- t2のテストの前に移動
        Games(
            team_id=t1,
            competition_type=competition_choices['甲子園'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['甲子園'])

        Games(
            team_id=t1,
            competition_type=competition_choices['甲子園'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['甲子園'])

        # 甲子園で敗戦 → 県大会（リセット）
        Games(
            team_id=t1,
            competition_type=competition_choices['甲子園'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        # ========================================================================
        # 引き分けのテストケース（夏のチーム）
        # ========================================================================
        # 夏の県大会で引き分け → 県大会継続
        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        # 夏の甲子園で引き分け → 甲子園継続
        Games(
            team_id=t1,
            competition_type=competition_choices['甲子園'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['甲子園'])

        # 秋のチーム
        Teams(year=1985, period=period['秋']).save()
        t2 = Teams.objects.latest('pk')
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['地区大会'])

        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['全国大会'])

        Games(
            team_id=t2,
            competition_type=competition_choices['センバツ'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['センバツ'])

        # 全国大会で敗戦 → センバツ（確定）
        Games(
            team_id=t2,
            competition_type=competition_choices['全国大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['センバツ'])

        # 全国大会決勝で勝利 → センバツ（確定）
        Games(
            team_id=t2,
            competition_type=competition_choices['全国大会'],
            competition_round=round_choices['決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['センバツ'])

        # ========================================================================
        # 引き分けのテストケース（秋のチーム）
        # ========================================================================
        # 秋の県大会で引き分け → 県大会継続
        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        # 秋の地区大会で引き分け → 地区大会継続
        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['地区大会'])

        # 秋の全国大会で引き分け → 全国大会継続
        Games(
            team_id=t2,
            competition_type=competition_choices['全国大会'],
            competition_round=round_choices['準決勝'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['全国大会'])

        # 秋のセンバツで引き分け → センバツ継続
        Games(
            team_id=t2,
            competition_type=competition_choices['センバツ'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['センバツ'])

        # ========================================================================
        # 秋の県大会1回戦のテストケース
        # ========================================================================
        # 秋の県大会1回戦で勝利 → 県大会継続
        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        # ========================================================================
        # 秋の地区大会1回戦のテストケース
        # ========================================================================
        # 秋の地区大会1回戦で勝利 → 地区大会継続
        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['地区大会'])

        # 秋の地区大会1回戦で敗戦 → 県大会（リセット）
        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['1回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

        # ========================================================================
        # 秋の全国大会の継続テストケース
        # ========================================================================
        # 秋の全国大会2回戦で勝利 → 全国大会継続（回戦は準決勝に進む）
        Games(
            team_id=t2,
            competition_type=competition_choices['全国大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['全国大会'])

        # 秋の全国大会準決勝で勝利 → 全国大会継続（回戦は決勝に進む）
        Games(
            team_id=t2,
            competition_type=competition_choices['全国大会'],
            competition_round=round_choices['準決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['全国大会'])

        # 秋の全国大会準決勝で引き分け → 全国大会継続
        Games(
            team_id=t2,
            competition_type=competition_choices['全国大会'],
            competition_round=round_choices['準決勝'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['全国大会'])

        # ========================================================================
        # 秋の県大会1回戦で敗戦のテストケース
        # ========================================================================
        # 秋の県大会1回戦で敗戦 → 県大会（リセット）
        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['1回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_type(),
            competition_choices['県大会'])

    def test_create_default_competition_round(self):
        """
        現在のチームに紐づくGamesのレコードが存在しない場合 -> 2(1回戦)
        現在のそのチームに紐づくGamesのレコードが存在する場合
            最新が練習試合 -> 2(1回戦)
            練習試合以外 -> 基本は前の試合で勝っていれば+1を設定する
                例外:
                    前の試合が負 であれば 2(1回戦)
                    前の試合が決勝 であれば次は2(1回戦)
                    秋 and 県大会 and ２回戦 and 勝　であれば次は2(1回戦)
                    秋 and 地区大会 and ２回戦　であれば次は2(1回戦)
                妥協：
                    １回戦、３回戦がない場合は考慮しない
        """
        period = ChoicesFormatter.period_choices_to_dict()
        competition_choices = ChoicesFormatter.competition_choices_to_dict()
        round_choices = ChoicesFormatter.round_choices_to_dict()

        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])
        # 夏のチーム
        Teams(year=1985, period=period['夏']).save()

        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        t1 = Teams.objects.latest('pk')
        Games(
            team_id=t1,
            competition_type=competition_choices['練習試合'],
            competition_round=round_choices['練習試合']
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['3回戦'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['決勝'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        # 甲子園進出後の回戦テスト（夏のチーム）- t2のテストの前に移動
        Games(
            team_id=t1,
            competition_type=competition_choices['甲子園'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['2回戦'])

        Games(
            team_id=t1,
            competition_type=competition_choices['甲子園'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['3回戦'])

        # 甲子園決勝で勝利 → 1回戦（リセット、次の大会はない）
        Games(
            team_id=t1,
            competition_type=competition_choices['甲子園'],
            competition_round=round_choices['決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        # ========================================================================
        # 引き分けのテストケース（夏のチーム）
        # ========================================================================
        # 夏の県大会で引き分け → 同じ回戦（再試合）
        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        # 夏の甲子園で引き分け → 同じ回戦（再試合）
        Games(
            team_id=t1,
            competition_type=competition_choices['甲子園'],
            competition_round=round_choices['準々決勝'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['準々決勝'])

        # ========================================================================
        # 夏の回戦進行の通常パターンの追加テストケース
        # ========================================================================
        # 夏の県大会3回戦で勝利 → 準々決勝
        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['3回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['準々決勝'])

        # 夏の県大会準々決勝で勝利 → 準決勝
        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['準々決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['準決勝'])

        # 夏の県大会準決勝で勝利 → 決勝
        Games(
            team_id=t1,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['準決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['決勝'])

        # 夏の甲子園3回戦で勝利 → 準々決勝
        Games(
            team_id=t1,
            competition_type=competition_choices['甲子園'],
            competition_round=round_choices['3回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['準々決勝'])

        # 夏の甲子園準々決勝で勝利 → 準決勝
        Games(
            team_id=t1,
            competition_type=competition_choices['甲子園'],
            competition_round=round_choices['準々決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['準決勝'])

        # 夏の甲子園準決勝で勝利 → 決勝
        Games(
            team_id=t1,
            competition_type=competition_choices['甲子園'],
            competition_round=round_choices['準決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['決勝'])

        # 秋のチーム
        Teams(year=1985, period=period['秋']).save()
        t2 = Teams.objects.latest('pk')
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['2回戦'])

        Games(
            team_id=t2,
            competition_type=competition_choices['全国大会'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['準決勝'])

        # 全国大会2回戦で敗戦 → センバツ1回戦
        Games(
            team_id=t2,
            competition_type=competition_choices['全国大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        # 全国大会決勝で勝利 → センバツ1回戦
        Games(
            team_id=t2,
            competition_type=competition_choices['全国大会'],
            competition_round=round_choices['決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        # センバツ進出後の回戦テスト
        Games(
            team_id=t2,
            competition_type=competition_choices['センバツ'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['2回戦'])

        Games(
            team_id=t2,
            competition_type=competition_choices['センバツ'],
            competition_round=round_choices['2回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['3回戦'])

        # センバツ決勝で勝利 → 1回戦（リセット、次の大会はない）
        Games(
            team_id=t2,
            competition_type=competition_choices['センバツ'],
            competition_round=round_choices['決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        # ========================================================================
        # 引き分けのテストケース（秋のチーム）
        # ========================================================================
        # 秋の県大会で引き分け → 同じ回戦（再試合）
        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        # 秋の地区大会で引き分け → 同じ回戦（再試合）
        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

        # 秋の全国大会で引き分け → 同じ回戦（再試合）
        Games(
            team_id=t2,
            competition_type=competition_choices['全国大会'],
            competition_round=round_choices['準決勝'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['準決勝'])

        # 秋のセンバツで引き分け → 同じ回戦（再試合）
        Games(
            team_id=t2,
            competition_type=competition_choices['センバツ'],
            competition_round=round_choices['3回戦'],
            score=1,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['3回戦'])

        # ========================================================================
        # 秋の回戦進行の通常パターンのテストケース
        # ========================================================================
        # 秋の県大会1回戦で勝利 → 2回戦
        Games(
            team_id=t2,
            competition_type=competition_choices['県大会'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['2回戦'])

        # 秋の地区大会1回戦で勝利 → 2回戦
        Games(
            team_id=t2,
            competition_type=competition_choices['地区大会'],
            competition_round=round_choices['1回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['2回戦'])

        # 秋の全国大会準決勝で勝利 → 決勝
        Games(
            team_id=t2,
            competition_type=competition_choices['全国大会'],
            competition_round=round_choices['準決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['決勝'])

        # 秋のセンバツ3回戦で勝利 → 準々決勝
        Games(
            team_id=t2,
            competition_type=competition_choices['センバツ'],
            competition_round=round_choices['3回戦'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['準々決勝'])

        # 秋のセンバツ準々決勝で勝利 → 準決勝
        Games(
            team_id=t2,
            competition_type=competition_choices['センバツ'],
            competition_round=round_choices['準々決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['準決勝'])

        # 秋のセンバツ準決勝で勝利 → 決勝
        Games(
            team_id=t2,
            competition_type=competition_choices['センバツ'],
            competition_round=round_choices['準決勝'],
            score=1,
            run=0
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['決勝'])

        # ========================================================================
        # 全国大会2回戦で敗戦のテストケース（回戦）
        # ========================================================================
        # 秋の全国大会2回戦で敗戦 → 1回戦（リセット）
        Games(
            team_id=t2,
            competition_type=competition_choices['全国大会'],
            competition_round=round_choices['2回戦'],
            score=0,
            run=1
        ).save()
        self.assertEqual(
            defaults.create_default_competition_round(),
            round_choices['1回戦'])

    def test_create_default_team_rank(self):
        """
        Gamesにレコードが存在しない場合   -> 0(初期値)
        Gamesにレコードが存在している場合 -> 最新レコードのrankと同じ値を返す
        """
        self.assertEqual(defaults.create_default_team_rank(), 0)
        Teams(year=1985, period=1).save()
        t1 = Teams.objects.latest('pk')
        Games(team_id=t1, rank=1).save()
        self.assertEqual(defaults.create_default_team_rank(), 1)
        Teams(year=1985, period=2).save()
        t2 = Teams.objects.latest('pk')
        Games(team_id=t2, rank=5).save()
        self.assertEqual(defaults.create_default_team_rank(), 5)

    def test_select_display_players(self):
        """
        Teamsにレコードが存在しない場合
            -> 空の辞書を返す
        ModelSettingsのis_used_limit_choices_toがTrue
            -> 空の辞書を返す
        eamsにレコードが存在して、最新レコードが
            period == 1(夏)
                -> {"admission_year__gte": teams.year - 2,
                    "admission_year__lte": teams.year}
                   -> 3学年分表示させる
            period == 2(秋)
                -> {"admission_year__gte": teams.year - 1,
                    "admission_year__lte": teams.year}
                    -> 2学年分表示させる
        """
        self.assertEqual(defaults.select_display_players(), {})
        Teams(year=1985, period=1).save()
        self.assertEqual(defaults.select_display_players(), {
                         "admission_year__gte": 1983, "admission_year__lte": 1985})
        Teams(year=1985, period=2).save()
        self.assertEqual(defaults.select_display_players(), {
                         "admission_year__gte": 1984, "admission_year__lte": 1985})
        ModelSettings(is_used_limit_choices_to=True).save()
        self.assertEqual(defaults.select_display_players(), {})
        ModelSettings(is_used_limit_choices_to=False).save()
        self.assertEqual(defaults.select_display_players(), {
                         "admission_year__gte": 1984, "admission_year__lte": 1985})

    def test_select_display_pitchers(self):
        """
        Teamsにレコードが存在しない場合
            -> 空の辞書を返す
        ModelSettingsのis_used_limit_choices_toがTrue
            -> 空の辞書を返す
        eamsにレコードが存在して、最新レコードが
            period == 1(夏)
                -> {"is_pitcher": True,
                    "admission_year__gte": teams.year - 2,
                    "admission_year__lte": teams.year}
                   -> 3学年分表示させる
            period == 2(秋)
                -> {"is_pitcher": True,
                    "admission_year__gte": teams.year - 1,
                    "admission_year__lte": teams.year}
                    -> 2学年分表示させる
        """
        self.assertEqual(
            defaults.select_display_pitchers(), {
                "is_pitcher": True})
        Teams(year=1998, period=1).save()
        self.assertEqual(defaults.select_display_pitchers(), {
                         "is_pitcher": True, "admission_year__gte": 1996, "admission_year__lte": 1998})
        Teams(year=1998, period=2).save()
        self.assertEqual(defaults.select_display_pitchers(), {
                         "is_pitcher": True, "admission_year__gte": 1997, "admission_year__lte": 1998})
        ModelSettings(is_used_limit_choices_to=True).save()
        self.assertEqual(
            defaults.select_display_pitchers(), {
                "is_pitcher": True})
        ModelSettings(is_used_limit_choices_to=False).save()
        self.assertEqual(defaults.select_display_pitchers(), {
                         "is_pitcher": True, "admission_year__gte": 1997, "admission_year__lte": 1998})


class SavedValueExtractorTests(TestCase):
    def test_create_game_results(self):
        """
        score > run  -> 1(勝)
        score < run  -> 2(負)
        score == run -> 3(分)
        """
        self.assertEqual(
            SavedValueExtractor.create_game_results(0, 0), 3)
        self.assertEqual(
            SavedValueExtractor.create_game_results(10, 10), 3)
        self.assertEqual(
            SavedValueExtractor.create_game_results(1, 0), 1)
        self.assertEqual(
            SavedValueExtractor.create_game_results(8, 7), 1)
        self.assertEqual(
            SavedValueExtractor.create_game_results(0, 1), 2)
        self.assertEqual(
            SavedValueExtractor.create_game_results(3, 4), 2)

    def test_update_is_pitcher(self):
        """
        positionが1(投手) または is_pitchedがTrue（野手だけど登板した）の場合はTrue
        """
        self.assertTrue(SavedValueExtractor.update_is_pitcher(1, True))
        self.assertTrue(SavedValueExtractor.update_is_pitcher(1, False))
        self.assertTrue(SavedValueExtractor.update_is_pitcher(2, True))
        self.assertFalse(SavedValueExtractor.update_is_pitcher(2, False))

    def test_check_is_cold_game(self):
        """
        県大会決勝、甲子園の場合はis_cold_gameがTrueだった場合、Falseに修正して保存する
        """
        self.assertTrue(
            SavedValueExtractor.check_is_cold_game(True, 1, 1))
        self.assertFalse(
            SavedValueExtractor.check_is_cold_game(False, 1, 1))
        self.assertTrue(
            SavedValueExtractor.check_is_cold_game(True, 2, 2))
        self.assertFalse(
            SavedValueExtractor.check_is_cold_game(False, 2, 2))
        self.assertTrue(
            SavedValueExtractor.check_is_cold_game(True, 2, 6))
        self.assertFalse(
            SavedValueExtractor.check_is_cold_game(False, 2, 6))
        self.assertFalse(
            SavedValueExtractor.check_is_cold_game(True, 2, 7))
        self.assertFalse(
            SavedValueExtractor.check_is_cold_game(False, 2, 7))
        self.assertTrue(
            SavedValueExtractor.check_is_cold_game(True, 3, 1))
        self.assertFalse(
            SavedValueExtractor.check_is_cold_game(False, 3, 1))
        self.assertTrue(
            SavedValueExtractor.check_is_cold_game(True, 4, 1))
        self.assertFalse(
            SavedValueExtractor.check_is_cold_game(False, 4, 1))
        self.assertFalse(
            SavedValueExtractor.check_is_cold_game(True, 5, 1))
        self.assertFalse(
            SavedValueExtractor.check_is_cold_game(False, 5, 1))
        self.assertFalse(
            SavedValueExtractor.check_is_cold_game(True, 6, 1))
        self.assertFalse(
            SavedValueExtractor.check_is_cold_game(False, 6, 1))


class ChoicesFormatterTests(TestCase):
    def test_competition_choices_to_dict(self):
        self.assertEqual(
            ChoicesFormatter.competition_choices_to_dict(),
            {'選択': '', '練習試合': 1, '県大会': 2, '地区大会': 3, '全国大会': 4, '甲子園': 5, 'センバツ': 6})

    def test_round_choices_to_dict(self):
        self.assertEqual(
            ChoicesFormatter.round_choices_to_dict(), {
                '選択': '', '練習試合': 1, '1回戦': 2, '2回戦': 3, '3回戦': 4, '準々決勝': 5, '準決勝': 6, '決勝': 7})

    def test_result_choices_to_dict(self):
        self.assertEqual(
            ChoicesFormatter.result_choices_to_dict(),
            {'選択': '', '勝': 1, '負': 2, '分': 3}
        )

    def test_rank_choices_to_dict(self):
        self.assertEqual(
            ChoicesFormatter.rank_choices_to_dict(), {
                '選択': '', '弱小': 1, 'そこそこ': 2, '中堅': 3, '強豪': 4, '名門': 5})

    def test_period_choices_to_dict(self):
        self.assertEqual(
            ChoicesFormatter.period_choices_to_dict(),
            {'選択': '', '夏': 1, '秋': 2}
        )

    def test_position_choices_to_dict(self):
        self.assertEqual(
            ChoicesFormatter.position_choices_to_dict(),
            {'選択': '', '投': 1, '捕': 2, '一': 3, '二': 4, '三': 5, '遊': 6, '外': 7}
        )
