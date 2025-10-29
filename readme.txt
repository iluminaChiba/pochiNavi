pochiNaviのセットアップ方法

1. windows に python がインストールされているかどうかを確認する。

$ python --version

2. 上のコマンドで毒を吐かれた場合は、インストールされていません。公式からインストールして下さい。
　 その節は、pythonインストールディレクトリにパスを通す、という項目にチェックするのをお忘れなく。

3. インストールされているのを確認したら、pipで以下の二つのモジュールを一気にインストール
   selenium はスクリプト言語でブラウザのコントロールを行う汎用のモジュール
   webdriver-manager は、Chrome用のドライバーを自動的に最新版に更新してくれる神ツールです

$ pip install selenium webdriver-manager

4. 同梱されているconfig.jsonファイルをエディターで開いて、自分の番号を入力
{
    "key1": 111,  <<<ここの数字を自分の数字に変更
    "key2": 222,
    "key3": 333
}

5. スクリプトを実行する。

$ python pochiNavi

run_pochiNavi.bat という名前で windows用batファイルも作ってあります。
batファイルのショートカットをデスクトップにでも作っておけば、ダブルクリックで起動します。