import streamlit as st
from models import init_db, get_user_urls
from auth import register, login
from urls import shorten_url, shorten_url_with_campaign
from utils import redirect_url
from analytics import get_click_analytics


def show_analytics():
  if st.session_state.logged_in:
    user_id = st.session_state.user.id
    urls = get_user_urls(user_id)

    selected_url = st.selectbox("短縮URLを選択", [url[1] for url in urls])
    if selected_url:
      analytics_data = get_click_analytics(selected_url)

      if analytics_data:
        total_clicks = sum(data[0] for data in analytics_data)
        unique_visitors = len(set(data[1] for data in analytics_data))

        st.write(f"総クリック数: {total_clicks}")
        st.write(f"ユニーク訪問者数: {unique_visitors}")

        # ... (他の分析データの表示) ...
      else:
        st.info("まだクリックデータがありません。")
    else:
      st.warning("短縮URLが選択されていません。")
  else:
    st.warning("この機能を使用するにはログインが必要です。")

    def main():
      st.title("URL Shortener")

      if not hasattr(st.session_state, "logged_in"):
        st.session_state.logged_in = False

      menu = ["ユーザー登録", "ログイン", "URL短縮", "キャンペーンパラメータ付きURL短縮", "分析情報"]
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
      elif choice == "分析情報":
        show_analytics()

      if not choice.startswith(
          "URL短縮") and "url" in st.experimental_get_query_params():
        short_url_id = st.experimental_get_query_params()["url"][0]
        redirect_url(short_url_id)


if __name__ == "__main__":
  init_db()
  main()
