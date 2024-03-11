import streamlit as st
import validators
import string
import random
from models import get_original_url, save_url_mapping


def shorten_url():
  st.subheader("URL短縮")
  original_url = st.text_input("短縮するURLを入力してください:")

  if st.button("短縮"):
    if not validators.url(original_url):
      st.error("有効なURLを入力してください。")
    else:
      short_url_id = generate_unique_short_url(original_url)
      save_url_mapping(original_url, short_url_id)
      short_url = f"{st.query_params.get('host', [''])[0]}?url={short_url_id}"
      st.success(f"短縮URL: {short_url}")


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
      short_url_id = generate_unique_short_url(long_url)
      save_url_mapping(long_url, short_url_id)
      short_url = f"{st.query_params.get('host', [''])[0]}?url={short_url_id}"
      st.success(f"短縮URL: {short_url}")


def generate_unique_short_url(original_url):
  while True:
    short_url_id = generate_short_url_id()
    if not get_original_url(short_url_id):
      return short_url_id


def generate_short_url_id(length=8):
  characters = string.ascii_letters + string.digits
  short_url_id = ''.join(random.choice(characters) for _ in range(length))
  return short_url_id
