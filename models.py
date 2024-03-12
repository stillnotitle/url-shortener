import sqlite3
import logging

logger = logging.getLogger(__name__)

class User:
    def __init__(self, username, email, password_hash, id):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.id = id


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
                original_url TEXT NOT NULL,
                short_url TEXT NOT NULL,
                click_count INTEGER DEFAULT 0)""")
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
    
    # Add user_id column if it doesn't exist
    c.execute("""
        SELECT COUNT(*) 
        FROM pragma_table_info('urls')
        WHERE name = 'user_id'
    """)
    if c.fetchone()[0] == 0:
        c.execute("ALTER TABLE urls ADD COLUMN user_id INTEGER")
    
    # Add click_count column if it doesn't exist
    c.execute("""
        SELECT COUNT(*)
        FROM pragma_table_info('urls')
        WHERE name = 'click_count'
    """)
    if c.fetchone()[0] == 0:
        c.execute("ALTER TABLE urls ADD COLUMN click_count INTEGER DEFAULT 0")
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect("urls.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_original_url(short_url_id):
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("SELECT original_url FROM urls WHERE short_url = ?", (short_url_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def save_url_mapping(original_url, short_url, user_id):
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    try:
        # 同じ元のURLが既に存在するかどうかを確認
        c.execute("SELECT short_url FROM urls WHERE original_url = ?", (original_url,))
        existing_short_url = c.fetchone()
        
        if existing_short_url:
            # 既存の短縮URLを返す
            return existing_short_url[0]
        else:
            # 新しい短縮URLを保存
            c.execute(
                "INSERT INTO urls (user_id, original_url, short_url) VALUES (?, ?, ?)",
                (user_id, original_url, short_url))
            conn.commit()
            logger.info(f"URL mapping saved: {original_url} -> {short_url}")
            return short_url
    except sqlite3.Error as e:
        logger.error(f"Error saving URL mapping: {e}")
        conn.rollback()
        return None
    finally:
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

def save_click_data(short_url, referer, user_agent, ip_address):
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    timestamp = datetime.now()
    c.execute(
        "INSERT INTO clicks (short_url, referer, user_agent, ip_address, timestamp) VALUES (?, ?, ?, ?, ?)",
        (short_url, referer, user_agent, ip_address, timestamp)
    )
    conn.commit()
    conn.close()

def get_click_analytics(short_url):
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("SELECT click_count, referer, user_agent FROM clicks WHERE short_url = ?", (short_url,))
    analytics_data = c.fetchall()
    conn.close()
    return analytics_data