# URL Shortener

このアプリケーションは、PythonとStreamlitを使用して構築されたシンプルなURLショートナーです。長いURLに対して短縮されたURLを作成することができ、短縮されたURLを管理してアクセスするためのユーザーフレンドリーなインターフェースを提供します。

## サンプルアプリ

[https://url-shortener.streamlit.app/](https://shrturl.streamlit.app/)

## 機能

- ユーザー登録とログイン機能
- オプションのカスタムURLを使用したURL短縮
- UTMトラッキングのためのキャンペーンパラメータサポート
- クリックトラッキングと分析
- Altairを使用したグラフによるクリック分析の可視化
- 分析テストのための手動クリック登録
- エラー処理とログ記録

## インストール

1. リポジトリをクローンします:

   ```
   git clone https://github.com/stillnotitle/url-shortener.git
   ```

2. プロジェクトディレクトリに移動します:

   ```
   cd url-shortener
   ```

3. 仮想環境を作成します:

   ```
   python -m venv venv
   ```

4. 仮想環境をアクティベートします:

   - Windowsの場合:

     ```
     venv\Scripts\activate
     ```

   - macOSとLinuxの場合:

     ```
     source venv/bin/activate
     ```

5. 必要な依存関係をインストールします:

   ```
   pip install -r requirements.txt
   ```

## 使用方法

1. アプリケーションを実行します:

   ```
   streamlit run app.py
   ```

2. ウェブブラウザを開き、`http://localhost:8501`にアクセスしてアプリケーションを使用します。

3. 新しいアカウントを登録するか、既存のアカウントにログインします。

4. サイドバーから目的のアクションを選択します:

   - **URL短縮**: 長いURLを入力し、必要に応じてカスタムの短いURLを指定します。"短縮"ボタンをクリックして、短縮されたURLを生成します。
   - **キャンペーンパラメータ付きURL短縮**: ウェブサイトのURLとキャンペーンパラメータ（UTMソース、メディア、キャンペーン、ターム、コンテンツ）を入力します。"短縮URLを生成"ボタンをクリックして、パラメータ付きの短縮URLを生成します。
   - **分析**: ドロップダウンから短縮URLを選択して、そのクリック分析を表示します。合計クリック数、ユニークビジター数、クリックトレンド、リファラー分布が表示されます。
   - **手動クリック登録**: 短縮URL、リファラー、ユーザーエージェント、IPアドレスを入力して、テスト目的でクリックを手動で登録します。

## 今後の機能拡張

- ユーザー固有の短縮URLリストと管理機能の実装
- URL有効期限機能の追加
- 短縮URLをプログラムで作成してアクセスするためのAPIエンドポイントの公開
- より多くのスタイリングとビジュアル要素によるユーザーインターフェースのさらなる改善
- デプロイとスケーラビリティを容易にするためのアプリケーションのDockerize

## 貢献

貢献は大歓迎です！問題を見つけたり、改善のための提案がある場合は、Issueを開くかPull Requestを提出してください。

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。

## 謝辞

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [SQLite](https://www.sqlite.org/)
- [Validators](https://validators.readthedocs.io/)
- [Altair](https://altair-viz.github.io/)
