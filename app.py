import streamlit as st
import altair as alt
import pandas as pd
from models import init_db, get_user_urls
from auth import register, login
from urls import shorten_url, shorten_url_with_campaign, BASE_URL
from utils import redirect_url
from analytics import get_click_analytics
from analytics import track_click
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def show_analytics():
    if st.session_state.logged_in:
        user_id = st.session_state.user.id
        urls = get_user_urls(user_id)

        selected_url = st.selectbox("短縮URLを選択", [url[1] for url in urls])
        if selected_url:
            short_url = f"{BASE_URL}?url={selected_url}"
            analytics_data = get_click_analytics(short_url)

            if analytics_data:
                df = pd.DataFrame(analytics_data, columns=['total_clicks', 'unique_visitors', 'referer', 'user_agent', 'click_date'])
                
                total_clicks = df['total_clicks'].sum()
                unique_visitors = df['unique_visitors'].sum()

                st.write(f"総クリック数: {total_clicks}")
                st.write(f"ユニーク訪問者数: {unique_visitors}")

                # クリック数の推移グラフ
                clicks_by_date = df.groupby('click_date')['total_clicks'].sum().reset_index()
                clicks_chart = alt.Chart(clicks_by_date).mark_line().encode(
                    x='click_date',
                    y='total_clicks'
                ).properties(title='クリック数の推移')
                st.altair_chart(clicks_chart, use_container_width=True)

                # リファラーの割合グラフ
                referrers = df.groupby('referer')['total_clicks'].sum().reset_index()
                referrers_chart = alt.Chart(referrers).mark_bar().encode(
                    x='referer',
                    y='total_clicks'
                ).properties(title='リファラー別クリック数')
                st.altair_chart(referrers_chart, use_container_width=True)

            else:
                st.info("まだクリックデータがありません。")
        else:
            st.warning("短縮URLが選択されていません。")
    else:
        st.warning("この機能を使用するにはログインが必要です。")

def manual_click_registration():
    st.subheader("手動クリックデータ登録")
    short_url = st.text_input("短縮URL")
    referer = st.text_input("リファラー")
    user_agent = st.text_input("ユーザーエージェント")
    ip_address = st.text_input("IPアドレス")

    if st.button("登録"):
        if short_url:
            track_click(short_url, referer, user_agent, ip_address)
            st.success("クリックデータが登録されました。")
        else:
            st.warning("短縮URLを入力してください。")

def main():
    st.title("URL Shortener")

    if not hasattr(st.session_state, "logged_in"):
        st.session_state.logged_in = False

    menu = ["ユーザー登録", "ログイン", "URL短縮", "キャンペーンパラメータ付きURL短縮", "分析情報", "手動クリックデータ登録"]
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
    elif choice == "手動クリックデータ登録":
        manual_click_registration()

    if not choice.startswith("URL短縮") and "url" in st.query_params:
        short_url_id = st.query_params["url"][0]
        redirect_url(short_url_id)

if __name__ == "__main__":
    init_db()
    main()