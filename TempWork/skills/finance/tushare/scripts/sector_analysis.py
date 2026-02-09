#!/usr/bin/env python3
"""
Tushare Sector Analysis Script
分析A股市场各板块表现，找出近期上升趋势的板块
"""

import sys
import json
import os
from datetime import datetime, timedelta

def get_tushare_pro():
    """获取Tushare Pro接口"""
    try:
        import tushare as ts
    except ImportError:
        print("错误: 请先安装 tushare: pip install tushare")
        sys.exit(1)
    
    token = os.environ.get('TUSHARE_TOKEN')
    if not token:
        # 尝试从配置文件读取
        config_path = os.path.expanduser('~/.tushare/config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                token = config.get('token')
    
    if not token:
        print("错误: 请设置 TUSHARE_TOKEN 环境变量或创建配置文件")
        print("获取token: https://tushare.pro/register")
        sys.exit(1)
    
    pro = ts.pro_api(token)
    return pro

def get_sector_performance(pro, days=5):
    """
    获取板块近期表现
    返回涨幅排名前20的板块
    """
    # 计算日期
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days+10)  # 多取几天避免节假日
    
    start_str = start_date.strftime('%Y%m%d')
    end_str = end_date.strftime('%Y%m%d')
    
    try:
        # 获取行业分类
        industries = pro.ths_index()
        
        results = []
        
        # 对每个行业获取近期数据
        for _, row in industries.head(30).iterrows():  # 限制数量避免API限制
            try:
                code = row['ts_code']
                name = row['name']
                
                # 获取行业日线数据
                df = pro.ths_daily(ts_code=code, start_date=start_str, end_date=end_str)
                
                if len(df) >= 2:
                    # 计算涨跌幅
                    latest = df.iloc[0]
                    prev = df.iloc[-1]
                    change_pct = (latest['close'] - prev['close']) / prev['close'] * 100
                    
                    results.append({
                        'code': code,
                        'name': name,
                        'change_pct': round(change_pct, 2),
                        'latest_close': latest['close'],
                        'volume': latest.get('vol', 0)
                    })
            except Exception as e:
                continue
        
        # 按涨跌幅排序
        results.sort(key=lambda x: x['change_pct'], reverse=True)
        return results[:20]
        
    except Exception as e:
        print(f"获取数据失败: {e}")
        return []

def get_concept_performance(pro, days=5):
    """
    获取概念板块近期表现
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days+10)
    
    start_str = start_date.strftime('%Y%m%d')
    end_str = end_date.strftime('%Y%m%d')
    
    try:
        # 获取概念指数
        concepts = pro.ths_index(type='N')
        
        results = []
        
        for _, row in concepts.head(30).iterrows():
            try:
                code = row['ts_code']
                name = row['name']
                
                df = pro.ths_daily(ts_code=code, start_date=start_str, end_date=end_str)
                
                if len(df) >= 2:
                    latest = df.iloc[0]
                    prev = df.iloc[-1]
                    change_pct = (latest['close'] - prev['close']) / prev['close'] * 100
                    
                    results.append({
                        'code': code,
                        'name': name,
                        'change_pct': round(change_pct, 2),
                        'type': '概念'
                    })
            except:
                continue
        
        results.sort(key=lambda x: x['change_pct'], reverse=True)
        return results[:15]
        
    except Exception as e:
        print(f"获取概念板块失败: {e}")
        return []

def main():
    print("=" * 60)
    print("A股市场板块趋势分析")
    print("=" * 60)
    print()
    
    pro = get_tushare_pro()
    
    # 获取近期表现（近5个交易日）
    print("【近期热门行业板块】(近5日涨幅)")
    print("-" * 60)
    
    sectors = get_sector_performance(pro, days=5)
    
    if sectors:
        for i, s in enumerate(sectors[:10], 1):
            trend = "📈" if s['change_pct'] > 0 else "📉"
            print(f"{i:2d}. {trend} {s['name'][:15]:15s} 涨幅: {s['change_pct']:+6.2f}%")
    else:
        print("暂无数据")
    
    print()
    print("【近期热门概念板块】(近5日涨幅)")
    print("-" * 60)
    
    concepts = get_concept_performance(pro, days=5)
    
    if concepts:
        for i, c in enumerate(concepts[:10], 1):
            trend = "📈" if c['change_pct'] > 0 else "📉"
            print(f"{i:2d}. {trend} {c['name'][:15]:15s} 涨幅: {c['change_pct']:+6.2f}%")
    else:
        print("暂无数据")
    
    print()
    print("=" * 60)
    print("提示: 以上数据仅供参考，不构成投资建议")
    print("=" * 60)

if __name__ == '__main__':
    main()
