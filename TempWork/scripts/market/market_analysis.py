import urllib.request
import json
import re
from datetime import datetime

def fetch_eastmoney_sectors():
    """从东方财富获取板块数据"""
    
    # 东方财富板块数据API
    url = "https://push2ex.eastmoney.com/getTopicZDFenBu?ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.zdfb"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://quote.eastmoney.com/',
        'Accept': 'application/json'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except Exception as e:
        print(f"获取板块数据失败: {e}")
        return None

def fetch_eastmoney_hot_stocks():
    """获取热门个股"""
    
    # 东方财富热股API
    url = "https://push2ex.eastmoney.com/getTopicZDT?ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.zdtb"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://quote.eastmoney.com/'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except Exception as e:
        print(f"获取热股数据失败: {e}")
        return None

def fetch_index_data():
    """获取主要指数数据"""
    
    # 东方财富指数API
    indices = [
        ('000001', '上证指数'),
        ('399001', '深证成指'),
        ('399006', '创业板指'),
        ('000300', '沪深300')
    ]
    
    results = []
    
    for code, name in indices:
        try:
            if code.startswith('6'):
                full_code = f"SH{code}"
            else:
                full_code = f"SZ{code}"
            
            url = f"https://push2.eastmoney.com/api/qt/stock/get?secid=1.{code}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://quote.eastmoney.com/'
            }
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read().decode('utf-8')
                json_data = json.loads(data)
                
                if json_data.get('data'):
                    d = json_data['data']
                    results.append({
                        'name': name,
                        'code': code,
                        'price': d.get('f43', 0) / 100 if d.get('f43') else 0,
                        'change': d.get('f44', 0) / 100 if d.get('f44') else 0,
                        'change_pct': d.get('f170', 0) / 100 if d.get('f170') else 0
                    })
        except Exception as e:
            print(f"获取{name}失败: {e}")
    
    return results

def main():
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 70)
    print("A股市场数据分析 - 东方财富数据源")
    print("时间: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("=" * 70)
    print()
    
    # 获取指数数据
    print("【主要指数表现】")
    print("-" * 70)
    indices = fetch_index_data()
    if indices:
        for idx in indices:
            trend = "UP" if idx['change'] >= 0 else "DOWN"
            print("{:<12} {:>10.2f}  {:+8.2f}  {:+6.2f}% [{}]".format(
                idx['name'], idx['price'], idx['change'], idx['change_pct'], trend))
    else:
        print("暂无指数数据")
    
    print()
    
    # 获取板块数据
    print("【热门板块】")
    print("-" * 70)
    sectors = fetch_eastmoney_sectors()
    if sectors and sectors.get('data'):
        for item in sectors['data'].get('diff', [])[:10]:
            name = item.get('f14', 'N/A')
            change_pct = item.get('f3', 0) / 100
            trend = "UP" if change_pct >= 0 else "DOWN"
            print("{:<15} {:+7.2f}% [{}]".format(name, change_pct, trend))
    else:
        print("暂无板块数据")
    
    print()
    print("=" * 70)
    print("提示: 以上数据来自东方财富公开接口")
    print("=" * 70)

if __name__ == '__main__':
    main()
