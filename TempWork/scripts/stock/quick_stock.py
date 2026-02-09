import urllib.request
import re

def get_stock(code):
    data = urllib.request.urlopen(f'http://qt.gtimg.cn/q={code}', timeout=10).read().decode('gbk', errors='ignore')
    match = re.search(r'v_.*?=\"(.*?)\";', data)
    if match:
        parts = match.group(1).split('~')
        return {
            'name': parts[1],
            'price': float(parts[3]),
            'yesterday': float(parts[4]),
            'change_pct': float(parts[32]) if parts[32] else 0
        }
    return None

indices = [('sh000001', '上证指数'), ('sz399001', '深证成指'), ('sz399006', '创业板指'), ('sh000300', '沪深300')]
print('=' * 60)
print('A股主要指数 (2026-02-09收盘)')
print('=' * 60)
for code, name in indices:
    try:
        s = get_stock(code)
        if s:
            change = s['price'] - s['yesterday']
            trend = 'UP' if change >= 0 else 'DOWN'
            print(f"{s['name']:<12} {s['price']:>10.2f}  {change:+8.2f}  {s['change_pct']:>6.2f}% [{trend}]")
    except Exception as e:
        print(f'{name}: 获取失败 - {e}')
