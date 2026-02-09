import urllib.request
import re
import sys

def parse_stock(data):
    """解析腾讯股票数据格式"""
    match = re.search(r'v_.*?=\"(.*?)\";', data)
    if match:
        parts = match.group(1).split('~')
        if len(parts) > 45:
            return {
                'name': parts[1],
                'code': parts[2],
                'price': float(parts[3]),
                'yesterday_close': float(parts[4]),
                'open': float(parts[5]),
                'volume': int(parts[6]) if parts[6] else 0,
                'high': float(parts[33]),
                'low': float(parts[34]),
                'change_pct': float(parts[32]) if parts[32] else 0
            }
    return None

def main():
    # 获取多个指数
    indices = [
        ('sh000001', '上证指数'),
        ('sz399001', '深证成指'),
        ('sz399006', '创业板指'),
        ('sh000300', '沪深300')
    ]
    
    print('=' * 60)
    print('A股主要指数 - 腾讯财经数据')
    print('=' * 60)
    print()
    
    for code, name in indices:
        try:
            url = f'http://qt.gtimg.cn/q={code}'
            data = urllib.request.urlopen(url, timeout=5).read().decode('gbk', errors='ignore')
            stock = parse_stock(data)
            if stock:
                change = stock['price'] - stock['yesterday_close']
                change_pct = stock['change_pct']
                trend = 'UP' if change >= 0 else 'DOWN'
                print(f"{stock['name']:<10} {stock['price']:>10.2f}  {change:+8.2f}  {change_pct:>6.2f}% [{trend}]")
        except Exception as e:
            print(f'{code}: 获取失败 - {e}')
    
    print()
    
    # 获取热门板块
    print('=' * 60)
    print('热门板块 - 东方财富')
    print('=' * 60)
    print()
    
    # 使用东方财富板块API
    try:
        # 行业板块
        url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f12,f14,f2,f3,f4,f5,f6,f7,f8,f9,f10,f18,f20,f21,f22,f23,f24,f25,f26,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42,f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91,f92,f93,f94,f95,f96,f97,f98,f99,f100"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://quote.eastmoney.com/'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('utf-8')
            import json
            json_data = json.loads(data)
            
            if json_data.get('data') and json_data['data'].get('diff'):
                print('【行业板块涨幅排行】')
                for i, item in enumerate(json_data['data']['diff'][:10], 1):
                    name = item.get('f14', 'N/A')
                    change_pct = item.get('f3', 0)
                    trend = 'UP' if change_pct >= 0 else 'DOWN'
                    print(f"{i:2d}. {name:<15} {change_pct:>+7.2f}% [{trend}]")
    except Exception as e:
        print(f'获取板块数据失败: {e}')
    
    print()
    print('=' * 60)

if __name__ == '__main__':
    main()
