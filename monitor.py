import os
import requests
import feedparser

# 從環境變數獲取 Secrets
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')
RSS_URL = os.getenv('RSS_URL')

def main():
    feed = feedparser.parse(RSS_URL)
    if not feed.entries:
        print("RSS 冇內容")
        return

    latest = feed.entries[0]
    title = latest.title
    link = latest.link

    # 檢查上次紀錄
    last_link = ""
    if os.path.exists("last_link.txt"):
        with open("last_link.txt", "r") as f:
            last_link = f.read().strip()

    if link != last_link:
        msg = f"🚨 <b>Hot Toys 有新消息！</b>\n\n內容：{title}\n\n連結：{link}"
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                      data={"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "HTML"})
        
        with open("last_link.txt", "w") as f:
            f.write(link)
        print(f"已發送通知：{title}")
    else:
        print("冇新 Post，跳過。")

if __name__ == "__main__":
    main()