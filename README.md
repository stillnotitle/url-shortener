# URL Shortener

このアプリケーションは、PythonとStreamlitを使って構築されたシンプルなURL短縮サービスです。長いURLを短いURLに変換し、短縮URLを管理・アクセスするためのユーザーフレンドリーなインターフェースを提供します。

## 機能

- 長いURLをコンパクトで共有しやすいURLに短縮
- カスタムURLのサポート：ユーザーは必要に応じてカスタムの短縮URLを指定可能
- リダイレクト：短縮URLをクリックすると元の長いURLにリダイレクト
- URLの検証：入力されたURLが有効であることを確認
- データベースストレージ：短縮URLと元のURLのマッピングをSQLiteデータベースに保存
- エラーハンドリング：無効な入力に対して分かりやすいエラーメッセージを表示

## インストール

1. リポジトリをクローン：
   ```
   git clone https://github.com/yourusername/url-shortener.git
   ```

2. プロジェクトディレクトリに移動：
   ```
   cd url-shortener
   ```

3. 仮想環境を作成：
   ```
   python -m venv venv
   ```

4. 仮想環境をアクティベート：
   - Windows の場合：
     ```
     venv\Scripts\activate
     ```
   - macOS と Linux の場合：
     ```
     source venv/bin/activate
     ```

5. 必要な依存関係をインストール：
   ```
   pip install -r requirements.txt
   ```

## 使い方

1. アプリケーションを起動：
   ```
   streamlit run app.py
   ```

2. Webブラウザを開き、`http://localhost:8501` にアクセスしてアプリケーションを使用。

3. 目的のアクションを選択：
   - URLを短縮するには、サイドバーから「Shorten URL」を選択し、長いURLを入力します。必要に応じてカスタムの短縮URLを指定できます。「Shorten」ボタンをクリックして、短縮URLを生成します。
   - 短縮URLにアクセスするには、サイドバーから「Redirect」を選択し、短縮URLを入力します。「Redirect」ボタンをクリックすると、元の長いURLにリダイレクトされます。

## 今後の改善点

- ユーザー認証：ユーザー登録とログイン機能を実装し、ユーザーが自分の短縮URLを管理できるようにする。
- URL の有効期限：短縮URLに有効期限を設定する機能を追加し、有効期限が切れると短縮URLにアクセスできなくなるようにする。
- クリックトラッキング：各短縮URLのクリック数を追跡し、ユーザーに分析情報を提供する。
- APIエンドポイント：短縮URLをプログラムで作成・アクセスするためのAPIエンドポイントを公開する。
- UIの改善：ユーザーエクスペリエンスを向上させるために、より多くのスタイリングと視覚的な要素を使ってユーザーインターフェースを強化する。
- コンテナ化：アプリケーションをDockerizeして、デプロイとスケーラビリティを容易にする。

## 貢献

貢献は大歓迎です！何か問題を見つけたり、改善のための提案がある場合は、Issueを開くかプルリクエストを送ってください。

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。

## 謝辞

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [SQLite](https://www.sqlite.org/)
- [Validators](https://validators.readthedocs.io/)

# URL Shortener

This is a simple URL shortener application built with Python and Streamlit. It allows users to create shortened URLs for long URLs and provides a user-friendly interface for managing and accessing the shortened URLs.

## Features

- Shorten long URLs into compact, easy-to-share URLs
- Custom URL support: Users can optionally specify a custom short URL
- Redirection: Shortened URLs redirect to the original long URLs
- URL validation: Ensures that the entered URLs are valid
- Database storage: Uses SQLite to store the mapping between short and long URLs
- Error handling: Provides informative error messages for invalid inputs

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/url-shortener.git
   ```

2. Change into the project directory:
   ```
   cd url-shortener
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - For Windows:
     ```
     venv\Scripts\activate
     ```
   - For macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   streamlit run app.py
   ```

2. Open a web browser and go to `http://localhost:8501` to access the application.

3. Choose the desired action:
   - To shorten a URL, select "Shorten URL" from the sidebar, enter the long URL, and optionally specify a custom short URL. Click the "Shorten" button to generate the shortened URL.
   - To access a shortened URL, select "Redirect" from the sidebar, enter the short URL, and click the "Redirect" button to be redirected to the original long URL.

## Future Enhancements

- User authentication: Implement user registration and login functionality to allow users to manage their own shortened URLs.
- URL expiration: Add the ability to set expiration dates for shortened URLs, after which they will no longer be accessible.
- Click tracking: Track the number of clicks on each shortened URL to provide analytics to users.
- API endpoints: Expose API endpoints for creating and accessing shortened URLs programmatically.
- UI improvements: Enhance the user interface with more styling and visual elements to provide a better user experience.
- Containerization: Dockerize the application for easier deployment and scalability.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [SQLite](https://www.sqlite.org/)
- [Validators](https://validators.readthedocs.io/)