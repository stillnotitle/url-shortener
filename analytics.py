import sqlite3
from datetime import datetime


def track_click(short_url, referer, user_agent, ip_address):
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute(
      """
        INSERT INTO clicks (short_url, referer, user_agent, ip_address, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (short_url, referer, user_agent, ip_address, datetime.now()))
  conn.commit()
  conn.close()


def get_click_analytics(short_url):
  conn = sqlite3.connect("urls.db")
  c = conn.cursor()
  c.execute(
      """
        SELECT COUNT(*) AS total_clicks, 
               COUNT(DISTINCT ip_address) AS unique_visitors,
               referer, 
               user_agent, 
               DATE(timestamp) AS click_date
        FROM clicks
        WHERE short_url = ?
        GROUP BY referer, user_agent, click_date
    """, (short_url, ))
  result = c.fetchall()
  conn.close()
  return result
