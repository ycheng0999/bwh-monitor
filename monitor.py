import os
import requests
import time

# 搬瓦工限量版商品 ID (145 为 $89.99 CN2 GIA-E 限量版)
PRODUCT_ID = "145"
MONITOR_URL = f"https://bwh81.net/cart.php?a=add&pid={PRODUCT_ID}"

# 从 GitHub Secrets 中读取 PUSH_KEY
PUSH_KEY = os.environ.get("PUSH_KEY")

# 模拟浏览器请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_notification():
    """发送 PushDeer 补货通知"""
    if PUSH_KEY:
        msg = "🔥 搬瓦工限量版（$89.99）补货了！速抢！\n直达链接：https://bwh81.net/aff.php?aff=1%26pid=145"
        url = f"https://api2.pushdeer.com/message/push?pushkey={PUSH_KEY}&text={msg}"
        try:
            # 限制发送通知请求在 10 秒内必须结束，防止因网络不好卡死
            requests.get(url, timeout=10)
            print("🔔 补货通知已成功发送至手机 PushDeer！")
        except Exception as e:
            print(f"❌ 发送通知失败: {e}")
    else:
        print("⚠️ 未检测到 PUSH_KEY，请检查仓库 Secrets 配置！")

def check_stock():
    """检测一次库存状态"""
    try:
        # 设置严格的 15 秒超时，防止搬瓦工官网网络卡死导致整个脚本停止
        response = requests.get(MONITOR_URL, headers=HEADERS, timeout=15)
        
        if "Out of Stock" in response.text:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ❌ 依然无货中...")
        else:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🔥 检测到有货了！！！")
            send_notification()
            
    except Exception as e:
        # 即使请求遇到网络异常（如超时），也捕获它并继续下一次检测，不让脚本崩溃
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ⚠️ 检测遇到异常(已自动跳过): {e}")

if __name__ == "__main__":
    print("🚀 高精度 5 分钟轮询监控已启动...")
    # 循环 58 次，每次间隔 5 分钟，总耗时约 290 分钟（4.8 小时）
    # 留出 10 分钟等待下一个任务自动来无缝接班
    for i in range(58):
        check_stock()
        time.sleep(300)
