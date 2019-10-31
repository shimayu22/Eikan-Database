# DBを検討する用

## データベース命名規約

https://qiita.com/genzouw/items/35022fa96c120e67c637

## 必要なテーブル
- players
- teams
- games
- fielder_results
- pitcher_results

## 項目

### teams
- id
- year(年度)
- period(夏、秋)
- prefecture(都道府県)
- training_policy(育成方針)
- draft_nomination(ドラフト指名人数)
- remark(備考)
- created_at
- updated_at

### players
- id
- admission_year(入学年度)
- name
- position
- remark
- created_at
- updated_at

### games
- id
- team_id
- competition_type(大会種類)
- round(n回戦)
- is_victory(勝ったか)
- score(得点)
- run(失点)
- lank(ランク)
- created_at
- updated_at

### fielder_results
- id
- game_id
- player_id
- at_bat
- run(得点)
- hit
- two_base
- three_base
- home_run
- run_batted_in(打点)
- strike_out(三振)
- bases_on_balls(四球)
- hit_by_pitch(死球)
- sacrifice_bunt(犠打)
- sacrifice_fly(犠飛)
- stolen_base(盗塁)
- grounded_into_double_play(併殺)
- error
- created_at
- updated_at

### pitcher_results
- id
- game_id
- player_id
- game(登板数)
- games_started(先発登板)
- innings_pitched(イニング)
- total_batters_faced(対戦打者)
- number_of_pitch(投球数)
- hit(被安打)
- strike_out(三振)
- bases_on_balls(四球)
- hit_by_pitch(死球)
- run(失点)
- earned_run(自責点)
- wild_pitch(暴投)
- home_run
- sacrifice_bunt(犠打)
- sacrifice_fly(犠飛)
- created_at
- updated_at