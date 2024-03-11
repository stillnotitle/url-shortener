import streamlit as st
import validators
import string
import random
from models import get_original_url, save_url_mapping

BASE_URL = "https://shrturl.streamlit.app/"

def shorten_url():
    st.subheader("URL短縮")
    original_url = st.text_input("短縮するURLを入力してください:")

    if st.button("短縮"):
        if not validators.url(original_url):
            st.error("有効なURLを入力してください。")
        else:
            short_url_id = generate_unique_short_url(original_url)
            if st.session_state.logged_in:
                user_id = st.session_state.user.id
            else:
                user_id = None
            save_url_mapping(original_url, short_url_id, user_id)
            short_url = f"{BASE_URL}?url={short_url_id}"
            st.success(f"短縮URL: {short_url}")

def shorten_url_with_campaign():
    st.subheader("キャンペーンパラメータ付きURL短縮")
    website_url = st.text_input("ウェブサイトURL", value="https://www.example.com")
    campaign_source = st.text_input("utm_source（必須）", help="プロパティにトラフィックを誘導した広告主、サイト、出版物、その他を識別します（Google、ニュースレター 4、屋外広告など）。")
    campaign_medium = st.text_input("utm_medium（必須）", help="広告メディアやマーケティング メディアを識別します（CPC 広告、バナー、メール ニュースレターなど）。")
    campaign_name = st.text_input("utm_campaign（必須）", help="商品のキャンペーン名、テーマ、プロモーション コードなどを指定します。")
    campaign_term = st.text_input("utm_term（オプション）", help="有料検索向けキーワードを特定します。検索広告キャンペーンにタグを設定する場合は、utm_term を使用してキーワードを指定することができます。")
    campaign_content = st.text_input("utm_content（オプション）", help="似通ったコンテンツや同じ広告内のリンクを区別するために使用します。たとえば、メールのメッセージに行動を促すフレーズのリンクが 2 つある場合は、utm_content を使用して別々の値を設定し、どちらが効果的か判断できます。")

    params = {
        "utm_source": campaign_source,
        "utm_medium": campaign_medium,
        "utm_campaign": campaign_name,
        "utm_term": campaign_term,
        "utm_content": campaign_content
    }
    params_str = "&".join(f"{k}={v}" for k, v in params.items() if v)
    long_url = f"{website_url}?{params_str}"

    st.write("プレビュー:")
    st.write(long_url)

    if st.button("短縮URLを生成"):
        if not validators.url(website_url):
            st.error("有効なURLを入力してください。")
        elif not campaign_source or not campaign_medium or not campaign_name:
            st.error("utm_source、utm_medium、utm_campaignは必須です。")
        else:
            short_url_id = generate_unique_short_url(long_url)
            if st.session_state.logged_in:
                user_id = st.session_state.user.id
            else:
                user_id = None
            save_url_mapping(long_url, short_url_id, user_id)
            short_url = f"{BASE_URL}?url={short_url_id}"
            st.success(f"短縮URL: {short_url}")

    st.write("注意事項:")
    st.write("- URL にパラメータを追加する際は、どのようなケースでも `utm_source`、`utm_medium`、`utm_campaign` を使用する必要があります。")
    st.write("- `utm_term` と `utm_content` は省略できます。")
    st.write("- `utm_` は、これらのパラメータ用の必須のプレフィックスです。")


def generate_unique_short_url(original_url):
  while True:
    short_url_id = generate_short_url_id()
    if not get_original_url(short_url_id):
      return short_url_id


def generate_short_url_id(length=8):
  characters = string.ascii_letters + string.digits
  short_url_id = ''.join(random.choice(characters) for _ in range(length))
  return short_url_id
