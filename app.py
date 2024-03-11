import streamlit as st
from models import init_db
from auth import register, login
from urls import shorten_url, shorten_url_with_campaign
from utils import redirect_url


def main():
  st.title("URL Shortener")

  if not hasattr(st.session_state, "logged_in"):
    st.session_state.logged_in = False

  menu = {
      "ユーザー登録": register,
      "ログイン": login,
      "URL短縮": shorten_url,
      "キャンペーンパラメータ付きURL短縮": shorten_url_with_campaign,
      "リダイレクト": redirect_url
  }

  choice = st.sidebar.radio("メニュー", list(menu.keys()))

  if choice == "ユーザー登録":
    register()
  elif choice == "ログイン":
    login()
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
  elif choice == "リダイレクト":
    redirect_url()


if __name__ == "__main__":
  init_db()
  main()
