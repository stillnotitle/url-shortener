import streamlit as st
import hashlib
import sqlite3
import validators
import string
import random

BASE_URL = "gvte.ch/"  # 短縮URLのベースURL

def init_db():
    """
    データベースの初期化
    """
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS urls
                 (original_url TEXT PRIMARY KEY, short_url TEXT)""")
    conn.commit()
    conn.close()

def save_url_to_db(original_url, short_url):
    """
    オリジナルURLと短縮URLをデータベースに保存
    """
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO urls VALUES (?, ?)", (original_url, short_url))
    conn.commit()
    conn.close()

def get_original_url(short_url_id):
    """
    短縮URLIDからオリジナルURLを取得
    """
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("SELECT original_url FROM urls WHERE short_url = ?", (short_url_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def generate_short_url_id(length=8):
    """
    指定された長さのランダムな短縮URLID（文字列）を生成
    """
    characters = string.ascii_letters + string.digits
    short_url_id = ''.join(random.choice(characters) for _ in range(length))
    return short_url_id

def generate_short_url(original_url):
    """
    オリジナルURLに対して短縮URLを生成
    """
    short_url_id = generate_short_url_id()
    short_url = BASE_URL + short_url_id
    return short_url

def generate_unique_short_url(original_url):
    """
    一意の短縮URLを生成
    """
    while True:
        short_url = generate_short_url(original_url)
        if not get_original_url(short_url.replace(BASE_URL, "")):
            return short_url

def is_valid_custom_url(custom_url):
    """
    カスタムURLが有効な形式かどうかを確認
    """
    allowed_chars = string.ascii_letters + string.digits + "-"
    return all(c in allowed_chars for c in custom_url)

def is_custom_url_available(custom_url):
    """
    カスタムURLが利用可能かどうかを確認
    """
    return not get_original_url(custom_url)

def main():
    """
    メイン関数、Streamlitアプリケーションの構成
    """
    st.title("URL Shortener")

    menu = ["Shorten URL", "Redirect"]
    choice = st.sidebar.radio("Select an option", menu)

    if choice == "Shorten URL":
        original_url = st.text_input("Enter the URL to shorten:")

        if original_url:
            if not validators.url(original_url):
                st.error("Invalid URL")
            else:
                custom_url = st.text_input("Custom URL (optional, 4-20 characters, letters, digits, and hyphens only):")

                if custom_url:
                    if len(custom_url) < 4 or len(custom_url) > 20:
                        st.error("Custom URL must be between 4 and 20 characters long")
                    elif not is_valid_custom_url(custom_url):
                        st.error("Custom URL can only contain letters, digits, and hyphens")
                    elif not is_custom_url_available(custom_url):
                        st.error("Custom URL is already in use")
                    else:
                        short_url = BASE_URL + custom_url
                        save_url_to_db(original_url, custom_url)
                        st.success(f"Shortened URL: {short_url}")
                else:
                    short_url = generate_unique_short_url(original_url)
                    save_url_to_db(original_url, short_url.replace(BASE_URL, ""))
                    st.success(f"Shortened URL: {short_url}")
    else:
        short_url = st.text_input("Enter the short URL:")
        if short_url:
            short_url_id = short_url.replace(BASE_URL, "")
            original_url = get_original_url(short_url_id)
            if original_url:
                st.success(f"Redirecting to: {original_url}")
            else:
                st.error("Invalid short URL")

if __name__ == "__main__":
    init_db()
    main()