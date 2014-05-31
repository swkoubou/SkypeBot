swkoubou.skype-bot
==================

　ソフトウェア工房身内用 SkypeBot です。  
　bot アカウントを招待したチャットウィンドウでコマンドを打つと、 Google Calendar 等の操作ができます。
　Python2.6で動作を確認しています。2.7でもたぶん動きます。  

Usage (Client)
------------------
　bot アカウントとの個人チャットを開くか、グループチャットに招待してください。  
　そのウィンドウで、`:g` から始まるコマンドを入力入力することにより、様々な操作ができます。  
　詳しくは `-h` もしくは `--help` オプションによるヘルプを参照してください。

- `:g calendar insert -s SUMMARY -b START -e END -t TIME_FLAG`:  GoogleCalendarに予定を追加します。  
  - `SUMMARY`: 予定の名前(必須)
  - `START`:開始時刻 (日本時間)(必須)
  - `END`: 終了時刻 (日本時間)(必須)
  - `TIME_FLAG`: 時間を指定するかどうか。`START`と`END`で要求されるフォーマットが変わる。(default: `true`)
     - `true`: yyyy-MM-ddThh:mm:ss   (e.g. 2014-05-31T18:30:00)
     - `false`: yyyy-MM-dd
- `:g calendar list`: GoogleCalendar に登録された予定一覧を表示する

Usage (Server)
-------------------
　OS は CentOS 6.5 minimal を想定しています。  
　ssh 等でサーバに接続し、下記の手順で認証と起動を行って下さい。  

1. `provisionning_script.sh` ファイルを参照又は実行し、必要なパッケージ等を全てインストールしてください(CentOS6.5 minimal 初期状態からのセットアップ確認済み)。  
2. 本リポジトリから python ファイルをコピーや git clone でサーバに取り込みます。  
3. `launch-skype.sh` 内の `USERNAME` と `PASSWORD` を skype の bot  用アカウントのものに変更します。  
4. `launch-skype.sh` を実行し、スカイプを実行します。  
5. Google Developers Console で、API を有効にして、ID等を取得します。  
6. 先ほど取得したID等を、`config.prop` ファイルに記述します。
5. `x11vnc -display :20 -xauth /var/run/skype/Xauthority &` コマンドでvncサービスを移動します。  
6. 別途クライアントを用意し、vnc クライアントでサーバに接続します。ポート番号はひとつ前のコマンド入力時に表示されます。  
7. GUI で Skype 認証画面が表示されているので、許可します。  
8. `env DISPLAY=:20 XAUTHORITY=/var/run/skype/Xauthority python skype-bot.py` で bot を起動します。  
9. GUI で Google API 認証画面が表示されるので、bot アカウントでログインして認証します。  
10. クライアントで bot アカウントとのチャット画面でコマンドを入力し、正常に動作していることを確認します。  

　お疲れ様です。SkypeBot が起動しました。  
　以降は手順4と手順8のみで起動できます。

Development & Test
------
　基本は `GoogleApiWrapper.py` を python のコマンドラインモード等で import してテストするといいと思います。 `skype-bot.py` から起動するには上記のような面倒なサーバ環境設定が必要です。  

####　実装について
　`GoogleAPIWrapper` クラスは基本は名前通り Google API をラップしているだけです。`ArgParse()` メソッドにコマンドライン引数を渡すと、あたかもコマンドラインから実行されたような動作をします。これは結果を標準出力・標準エラー出力に出力します。  
　`skype-bot.py` 内の `skype_handler()` 関数で skype からメッセージを受け取り、解析し、`:g` トリガーが見つかるとそれ以降の文字列を `GoogleApiWrapper` に渡しています。その前後で標準出力・標準エラー出力への出力を文字列バッファーへと切り替えて、Skypeチャットへ返しています。  
　つまり、開発は基本的に `GoogleAPIWrapper` クラス内を改善していくのが良いと思います。

#### argparser のサブコマンド処理について
　argparser でサブコマンドをいくつか生成していますが、解析結果からはどのサブコマンドが実行されたかの判断ができません。通常これはサブコマンド生成時にそれ用の関数を渡して対処するようですが、クラス内でうまく実装する方法が分からなかったため、最下層にオプションで判別用オプション(e.g. --calendar_insert)を付加して対処しています。

#### APIキーについて
　動作させるためには `config.prop` にAPIの情報を記述する必要がありますが、個人情報となりますので、そのまま GitHub に上げないように十分に注意してください。
