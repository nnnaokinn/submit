■Youtubeチャンネル情報一覧
バーチャルYoutuberのランキング等を参照できるUserLocal(https://virtual-youtuber.userlocal.jp/)に対してpythonスクリプトでスクレイピングを行い、
スクレイピング結果を基にYoutube Data APIで取得したチャンネル情報をベーシックなLamp環境で表示するツールです。

readme.txtのあるディレクトリで以下のコマンドを実行してください。
なお、手順2については外因（UserLocalの表示変更、Youtube Data APIの使用量制限）によって失敗するため、
予めMySQLにデータは投入しており、飛ばしても問題ありません。


1.Docker環境構築
docker-compose up -d --build


2.pythonの環境上でスクリプトを実行
docker-compose exec python bash
python GetYoutubeStatistics.py

※スクレイピング及びYoutube APIを大量に行うため非常に時間がかかります。
※MySQLが立ち上がりきっていない場合はエラーが発生します。


3.Webブラウザで以下のアドレスにアクセスしてバーチャルYoutuber情報を一覧表示
http://localhost:80

