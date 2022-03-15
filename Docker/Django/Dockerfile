FROM python:3.10-buster

# updateとvimのインストールを行う
RUN apt-get update && \
    apt-get install -y vim

# コンテナ側の作業用ディレクトリを指定する
WORKDIR /usr/local/src

# タイムゾーンをUTCからJSTに変更する
RUN ln -sf /usr/share/zeneinfo/Asia/Tokyo /etc/localtime

# 環境設定
# ローカルIPアドレスをDjangoに割り振るために指定
ENV HOST 0.0.0.0

# コンテナ実行時に所定ネットワーク上のどのポートをリッスンするかを指定する
# expose:露出する
EXPOSE 8000