import os
import requests

PRODUCT_ID = "145"
MONITOR_URL = f"https://bwh81.net/cart.php?a=add&pid={PRODUCT_ID}"
PUSH_KEY = os.environ.get("PUSH_KEY")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_notification():
    if PUSH_KEY:
        msg = "🔥 搬瓦工神机（$89.99 限量版）补货了！速抢！\n直达链接：https://bwh81.net/aff.php?aff=1%26pid=145"
        url = f"https://api2.pushdeer.com/message/push?pushkey={PUSH_KEY}&text={msg}"
        try:
            # 限制 5 秒内必须发送完毕
            requests.get(url, timeout=5)
            print("🔔 补货通知已发送至手机！")
        except Exception as e:
            print(f"发送通知失败: {e}")
    else:
        print("⚠️ 未配置 PUSH_KEY！")

def check_stock():
    try:
        # 加上严格的 timeout=5，防止请求卡死
        response = requests.get(MONITOR_URL, headers=HEADERS, timeout=5)
        if "Out of Stock" in response.text:
            print("❌ 依然无货中...")
        else:
            print("🔥 有货了！！！")
            send_notification()
    except Exception as e:
        print(f"检测异常(已自动跳过): {e}")

if __name__ == "__main__":
    check_stock()
