import streamlit as st
from models import get_original_url


def redirect_url(short_url_id):
  original_url = get_original_url(short_url_id)

  if original_url:
    st.redirect(original_url)
  else:
    st.error("無効な短縮URLです。")
