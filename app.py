import streamlit as st
from models import init_db
from auth import register, login
from urls import shorten_url, shorten_url_with_campaign
from utils import redirect_url


def main():
  st.title("URL Shortener")

  if not hasattr(st.session_state, "logged_in"):
    st.session_state.logged_in = False

  menu = ["ユーザー登録", "ログイン", "URL短縮", "キャンペーンパラメータ付きURL短縮"]
  choice = st.sidebar.radio("メニュー", menu)

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

  if "url" in st.experimental_get_query_params():
    short_url_id = st.experimental_get_query_params()["url"][0]
    redirect_url(short_url_id)


if __name__ == "__main__":
  init_db()
  main()
