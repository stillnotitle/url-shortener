import streamlit as st
from streamlit.components.v1 import html
from models import get_original_url
from analytics import track_click

def redirect_url(short_url_id):
    original_url = get_original_url(short_url_id)

    if original_url:
        referer = st.experimental_get_query_params().get("referer", [""])[0]
        user_agent = st.experimental_user_agent()
        ip_address = st.experimental_client_ip_address()
        track_click(short_url_id, referer, user_agent, ip_address)

        html_code = f'<meta http-equiv="refresh" content="0; url={original_url}">'
        html(html_code)
        st.stop()
    else:
        st.error("無効な短縮URLです。")