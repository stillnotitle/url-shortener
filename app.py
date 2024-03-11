import streamlit as st
import hashlib
import sqlite3
import validators
import string
import random
import re


# ユーザーモデルの定義
class User:

  def __init__(self, username, email, password_hash):
    self.username = username
    self.email = email
    self.password_hash = password_hash


# データベースの初期化
def init_db():
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute("""CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL UNIQUE,
                 email TEXT NOT NULL UNIQUE,
                 password_hash TEXT NOT NULL)""")
  c.execute("""CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 original_url TEXT NOT NULL,
                 short_url TEXT NOT NULL)""")
  conn.commit()
  conn.close()


# ユーザーの作成
def create_user(username, email, password):
  password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
  user = User(username, email, password_hash)
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute(
      "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
      (user.username, user.email, user.password_hash))
  conn.commit()
  conn.close()


# ユーザーの認証
def authenticate_user(username, password):
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute("SELECT * FROM users WHERE username = ?", (username, ))
  user = c.fetchone()
  conn.close()

  if user:
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if password_hash == user[3]:
      return User(user[1], user[2], user[3])

  return None


# ユーザー登録
def register():
  st.subheader("ユーザー登録")
  username = st.text_input("ユーザー名")
  email = st.text_input("メールアドレス")
  password = st.text_input("パスワード", type="password")
  confirm_password = st.text_input("パスワードの確認", type="password")

  if st.button("登録"):
    if not username or not email or not password or not confirm_password:
      st.error("すべての項目を入力してください。")
    elif password != confirm_password:
      st.error("パスワードが一致しません。")
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
      st.error("有効なメールアドレスを入力してください。")
    else:
      create_user(username, email, password)
      st.success("ユーザー登録が完了しました。")


# ログイン
def login():
  st.subheader("ログイン")
  username = st.text_input("ユーザー名")
  password = st.text_input("パスワード", type="password")

  if st.button("ログイン"):
    user = authenticate_user(username, password)
    if user:
      st.session_state.logged_in = True
      st.session_state.user = user
      st.success("ログインしました。")
    else:
      st.error("無効なユーザー名またはパスワードです。")


# URL短縮
def shorten_url():
  st.subheader("URL短縮")
  original_url = st.text_input("短縮するURLを入力してください:")

  if st.button("短縮"):
    if not validators.url(original_url):
      st.error("有効なURLを入力してください。")
    else:
      short_url = generate_unique_short_url(original_url)
      save_url_mapping(original_url, short_url)
      st.success(f"短縮URL: {short_url}")


# キャンペーンパラメータ付きURL短縮
def shorten_url_with_campaign():
  st.subheader("キャンペーンパラメータ付きURL短縮")
  website_url = st.text_input("ウェブサイトURL", value="https://www.example.com")
  campaign_id = st.text_input("キャンペーンID")
  campaign_source = st.text_input("キャンペーンソース")
  campaign_medium = st.text_input("キャンペーンメディア")
  campaign_name = st.text_input("キャンペーン名")
  campaign_term = st.text_input("キャンペーン期間")
  campaign_content = st.text_input("キャンペーンコンテンツ")

  if st.button("短縮URLを生成"):
    if not validators.url(website_url):
      st.error("有効なURLを入力してください。")
    else:
      params = {
          "utm_source": campaign_source,
          "utm_medium": campaign_medium,
          "utm_campaign": campaign_name,
          "utm_term": campaign_term,
          "utm_content": campaign_content,
          "utm_id": campaign_id
      }
      params_str = "&".join(f"{k}={v}" for k, v in params.items() if v)
      long_url = f"{website_url}?{params_str}"
      short_url = generate_unique_short_url(long_url)
      save_url_mapping(long_url, short_url)
      st.success(f"短縮URL: {short_url}")


# リダイレクト
def redirect():
  st.subheader("リダイレクト")
  short_url = st.text_input("短縮URLを入力してください:")
  if short_url:
    original_url = get_original_url(short_url.replace(BASE_URL, ""))
    if original_url:
      st.success(f"リダイレクト先: {original_url}")
    else:
      st.error("無効な短縮URLです。")


# 短縮URLの生成
def generate_unique_short_url(original_url):
  while True:
    short_url = BASE_URL + generate_short_url_id()
    if not get_original_url(short_url.replace(BASE_URL, "")):
      return short_url


# 短縮URLIDの生成
def generate_short_url_id(length=8):
  characters = string.ascii_letters + string.digits
  short_url_id = ''.join(random.choice(characters) for _ in range(length))
  return short_url_id


# オリジナルURLの取得
def get_original_url(short_url_id):
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute("SELECT original_url FROM urls WHERE short_url = ?",
            (short_url_id, ))
  result = c.fetchone()
  conn.close()
  return result[0] if result else None


# URLマッピングの保存
def save_url_mapping(original_url, short_url):
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)",
            (original_url, short_url))
  conn.commit()
  conn.close()


# メイン関数
def main():
  st.title("URL Shortener")

  if not hasattr(st.session_state, "logged_in"):
    st.session_state.logged_in = False

  menu = ["ログイン", "ユーザー登録", "URL短縮", "キャンペーンパラメータ付きURL短縮", "リダイレクト"]
  choice = st.sidebar.selectbox("選択してください", menu)

  if choice == "ログイン":
    login()
  elif choice == "ユーザー登録":
    register()
  elif choice == "URL短縮":
    if st.session_state.logged_in:
      shorten_url()
    else:
      st.warning("この機能を使用するにはログインが必要です。")
  elif choice == "キャンペーンパラメータ付きURL短縮":
    if st.session_state.logged_in:
      shorten_url_with_campaign()
    else:
      st.warning("この機能を使用するにはログインが必要です。")
  else:
    redirect()


if __name__ == "__main__":
  init_db()
  main()
