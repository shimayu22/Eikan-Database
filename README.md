# はじめに

本アプリケーションは、栄冠ナインのデータを入力、表示するアプリケーションです。

# 環境

- Python 3.7.4
- Django 2.2.6

# 初期設定

ひとまずvenvで動きます。

### Win版
    python -m venv env
    env\Sctipts\activate
    pip install -r requirements.txt
    manage.py migrate
    manage.py createsuperuser
    manage.py runserver

### Mac版
    python3 -m venv env
    source env\bin\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver


# 使い方

## 初期登録

1. http://127.0.0.1:8000/admin/eikan/teams/add/ より、チーム情報を入力する
1. http://127.0.0.1:8000/admin/eikan/players/add/ より、チーム全員の選手を入力する

## 試合を登録する

1. 試合終了後のリザルト画面のデータを開く
1. http://127.0.0.1:8000/admin/eikan/games/add/ より、試合情報を登録する

# 登録する情報について

- 年に2回チーム登録を行う
  - 夏（1〜３年）
  - 秋（１、２年）
  
- 新入生が入学してきたら選手情報に追加する

- 総合成績は試合情報に登録した値から自動的に計算されます

# ご注意
- 「とりあえず動く」状態です、適宜修正していきます
