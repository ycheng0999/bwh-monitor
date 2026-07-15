import os
import requests
import time

PRODUCT_ID = "145"
MONITOR_URL = f"https://bwh81.net/cart.php?a=add&pid={PRODUCT_ID}"
PUSH_KEY = os.environ.get("PUSH_KEY")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def send_notification():
    if PUSH_KEY:
        msg = "🔥 搬瓦工限量版补货了！速抢！\n直达链接：https://bwh81.net/aff.php?aff=1%26pid=145"
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
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ 依然无货中...")
        else:
            print("🔥 有货了！！！")
            send_notification()
    except Exception as e:
        print(f"检测异常: {e}")

if __name__ == "__main__":
    # 循环 58 次，每次间隔 300 秒（5分钟），总计运行约 290 分钟（4.8小时）
    # 留出 10 分钟空隙，等待下一个定时任务来无缝接班
    for i in range(58):
        check_stock()
        time.sleep(300)
