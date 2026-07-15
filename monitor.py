import os
import requests
import time

PRODUCT_ID = "145"
MONITOR_URL = f"https://bwh81.net/cart.php?a=add&pid={PRODUCT_ID}"
PUSH_KEY = os.environ.get("PUSH_KEY")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

def send_notification():
    if PUSH_KEY:
        msg = "🔥 搬瓦工限量版补货了！速抢！\n直达链接：https://bwh81.net/aff.php?aff=1%26pid=145"
        url = f"https://api2.pushdeer.com/message/push?pushkey={PUSH_KEY}&text={msg}"
        try:
            # 推送限制 5 秒超时
            requests.get(url, timeout=5)
            print("🔔 补货通知已发送至手机！")
        except Exception as e:
            print(f"发送通知失败: {e}")
    else:
        print("⚠️ 未检测到 PUSH_KEY")

def check_stock():
    try:
        # 检测网页限制 5 秒超时，防止卡死
        response = requests.get(MONITOR_URL, headers=HEADERS, timeout=5)
        if "Out of Stock" in response.text:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ 依然无货中...")
        else:
            print("🔥 有货了！！！")
            send_notification()
    except Exception as e:
        print(f"检测异常(已自动跳过): {e}")

if __name__ == "__main__":
    # 只运行一次，绝不挂起
    check_stock()
