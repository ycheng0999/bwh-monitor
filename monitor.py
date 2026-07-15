import os
import requests

# 搬瓦工限量版商品 ID (145 为 $89.99 CN2 GIA-E 限量版)
PRODUCT_ID = "145"
MONITOR_URL = f"https://bwh81.net/cart.php?a=add&pid={PRODUCT_ID}"

# 从 GitHub Secrets 中安全读取你的推送 Key
PUSH_KEY = os.environ.get("PUSH_KEY")

# 模拟浏览器请求头，防止被官网拦截
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_notification():
    """发送补货通知到你的手机 PushDeer"""
    if PUSH_KEY:
        # 抢购消息和直达链接
        msg = "🔥 搬瓦工神机（$89.99 限量版）补货了！速抢！\n直达链接：https://bwh81.net/aff.php?aff=1%26pid=145"
        url = f"https://api2.pushdeer.com/message/push?pushkey={PUSH_KEY}&text={msg}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("🔔 补货通知已成功发送至你的 PushDeer 手机端！")
            else:
                print(f"❌ 消息发送失败，接口返回状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ 发送通知时发生异常: {e}")
    else:
        print("⚠️ 未检测到 PUSH_KEY，请检查 GitHub Settings -> Secrets 中是否正确配置了 PUSH_KEY！")

def check_stock():
    """检测搬瓦工官网库存状态"""
    try:
        print("正在检测搬瓦工库存...")
        response = requests.get(MONITOR_URL, headers=HEADERS, timeout=15)
        
        # 搬瓦工无货时页面会显示 "Out of Stock"
        if "Out of Stock" in response.text:
            print("❌ 依然无货中...")
        else:
            print("🔥 检测到有货了！！！")
            send_notification()
            
    except Exception as e:
        print(f"❌ 请求搬瓦工官网出错: {e}")

if __name__ == "__main__":
    check_stock()
