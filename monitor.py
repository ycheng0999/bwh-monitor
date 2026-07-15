import os
import requests

PRODUCT_ID = "145"
MONITOR_URL = f"https://bwh81.net/cart.php?a=add&pid={PRODUCT_ID}"
PUSH_KEY = os.environ.get("PUSH_KEY")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def send_notification():
    if PUSH_KEY:
        msg = "🔥 搬瓦工神机（限量版）补货了！速抢！\n直达链接：https://bwh81.net/aff.php?aff=1%26pid=145"
        url = f"https://api2.pushdeer.com/message/push?pushkey={PUSH_KEY}&text={msg}"
        try:
            requests.get(url, timeout=10)
            print("🔔 补货通知已发送至手机！")
        except Exception as e:
            print(f"发送通知失败: {e}")

def check_stock():
    try:
        response = requests.get(MONITOR_URL, headers=HEADERS, timeout=15)
        if "Out of Stock" in response.text:
            print("❌ 依然无货中...")
        else:
            print("🔥 有货了！！！")
            send_notification()
    except Exception as e:
        print(f"检测异常: {e}")

if __name__ == "__main__":
    check_stock()
