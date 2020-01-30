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
    ren config\local_settings.txt local_settings.py
    python config/get_random_secret_key.py >> config/local_settings.py
    manage.py migrate
    manage.py createsuperuser
    manage.py runserver

### Mac版
    python3 -m venv env
    source env\bin\activate
    pip install -r requirements.txt
    mv config/local_settings.txt config/local_settings.py
    python config/get_random_secret_key.py >> config/local_settings.py
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
- 指標については以下の書籍を参考にしています
  - [セイバーメトリクス入門　　脱常識で野球を科学する](https://amzn.to/2GdxUgt)
  - [野球×統計は最強のバッテリーである - セイバーメトリクスとトラッキングの世界](https://amzn.to/2R3HBUE)
