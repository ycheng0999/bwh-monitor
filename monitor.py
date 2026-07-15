import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

PRODUCT_ID = "145"
# 更改点 1：GitHub 运行在海外，直接请求 bandwagonhost.com 速度最快且不卡顿
MONITOR_URL = f"https://bandwagonhost.com/cart.php?a=add&pid={PRODUCT_ID}"
PUSH_KEY = os.environ.get("PUSH_KEY")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_notification():
    if PUSH_KEY:
        msg = "🔥 搬瓦工神机（$89.99 限量版）补货了！速抢！\n直达链接：https://bwh81.net/aff.php?aff=1%26pid=145"
        url = f"https://api2.pushdeer.com/message/push?pushkey={PUSH_KEY}&text={msg}"
        try:
            requests.get(url, timeout=5)
            print("🔔 补货通知已发送至手机！")
        except Exception as e:
            print(f"发送通知失败: {e}")
    else:
        print("⚠️ 未配置 PUSH_KEY！")

def check_stock():
    # 建立一个带重试机制的 session
    session = requests.Session()
    retries = Retry(total=2, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        # 更改点 2：将 timeout 细化为 (连接超时, 读取超时)
        response = session.get(MONITOR_URL, headers=HEADERS, timeout=(3.05, 5))
        
        if "Out of Stock" in response.text:
            print("❌ 依然无货中...")
        else:
            print("🔥 有货了！！！")
            send_notification()
    except Exception as e:
        print(f"检测异常(已自动跳过): {e}")

if __name__ == "__main__":
    check_stock()
