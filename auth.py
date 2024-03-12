import streamlit as st
import hashlib
import sqlite3
import re
from models import User, save_url_mapping


def create_user(username, email, password):
  password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  try:
    c.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash))
    conn.commit()
    user_id = c.lastrowid # 新しく挿入された行のIDを取得
    return User(username, email, password_hash, user_id) # Userオブジェクトを返す
  except sqlite3.IntegrityError:
    return False
  finally:
    conn.close()


def authenticate_user(username, password):
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute("SELECT * FROM users WHERE username = ?", (username, ))
  user = c.fetchone()
  conn.close()

  if user:
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if password_hash == user[3]:
      return User(user[1], user[2], user[3], user[0]) # ユーザーIDを渡す

  return None


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
      if create_user(username, email, password):
        st.success("ユーザー登録が完了しました。")
      else:
        st.error("このユーザー名またはメールアドレスは既に使用されています。")


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
