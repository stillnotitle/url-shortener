import sqlite3


class User:

  def __init__(self, username, email, password_hash):
    self.username = username
    self.email = email
    self.password_hash = password_hash


def init_db():
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute("""CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL UNIQUE,
                 email TEXT NOT NULL UNIQUE,
                 password_hash TEXT NOT NULL)""")
  c.execute("""CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 original_url TEXT NOT NULL,
                 short_url TEXT NOT NULL,
                 click_count INTEGER DEFAULT 0,
                 FOREIGN KEY (user_id) REFERENCES users (id))""")
  c.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_url TEXT,
            referer TEXT,
            user_agent TEXT,
            ip_address TEXT,
            timestamp DATETIME
        )
    """)
  conn.commit()
  conn.close()


def get_original_url(short_url_id):
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute("SELECT original_url FROM urls WHERE short_url = ?",
            (short_url_id, ))
  result = c.fetchone()
  conn.close()
  return result[0] if result else None


def save_url_mapping(original_url, short_url, user_id):
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute(
      "INSERT INTO urls (user_id, original_url, short_url) VALUES (?, ?, ?)",
      (user_id, original_url, short_url))
  conn.commit()
  conn.close()


def get_user_urls(user_id):
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute(
      "SELECT original_url, short_url, click_count FROM urls WHERE user_id = ?",
      (user_id, ))
  urls = c.fetchall()
  conn.close()
  return urls


def save_url_mapping(original_url, short_url, user_id):
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute(
      "INSERT INTO urls (user_id, original_url, short_url) VALUES (?, ?, ?)",
      (user_id, original_url, short_url))
  conn.commit()
  conn.close()
