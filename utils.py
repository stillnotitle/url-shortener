import streamlit as st
from streamlit.components.v1 import html
from models import get_original_url


def redirect_url():
  short_url_id = st.query_params.get("url", [""])[0]
  original_url = get_original_url(short_url_id)

  if original_url:
    html(f'<meta http-equiv="refresh" content="0; url={original_url}">')
  else:
    st.error("無効な短縮URLです。")
