#!/usr/bin/env python3
"""
Tushare Market Trend Analysis
分析A股市场整体趋势
"""

import sys
import os
import json
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
        config_path = os.path.expanduser('~/.tushare/config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                token = config.get('token')
    
    if not token:
        print("错误: 请设置 TUSHARE_TOKEN 环境变量")
        print("获取token: https://tushare.pro/register")
        sys.exit(1)
    
    return ts.pro_api(token)

def get_index_trend(pro, index_code='000001.SH', name='上证指数'):
    """获取指数近期走势"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    try:
        df = pro.index_daily(ts_code=index_code, 
                            start_date=start_date.strftime('%Y%m%d'),
                            end_date=end_date.strftime('%Y%m%d'))
        
        if len(df) > 0:
            latest = df.iloc[0]
            # 计算5日、10日、20日涨跌幅
            change_5d = 0
            change_10d = 0
            change_20d = 0
            
            if len(df) >= 5:
                change_5d = (latest['close'] - df.iloc[4]['close']) / df.iloc[4]['close'] * 100
            if len(df) >= 10:
                change_10d = (latest['close'] - df.iloc[9]['close']) / df.iloc[9]['close'] * 100
            if len(df) >= 20:
                change_20d = (latest['close'] - df.iloc[19]['close']) / df.iloc[19]['close'] * 100
            
            return {
                'name': name,
                'latest': latest['close'],
                'change_5d': round(change_5d, 2),
                'change_10d': round(change_10d, 2),
                'change_20d': round(change_20d, 2),
                'volume': latest.get('amount', 0) / 100000000  # 成交额(亿)
            }
    except Exception as e:
        print(f"获取{name}数据失败: {e}")
    
    return None

def get_market_sentiment(pro):
    """获取市场情绪指标"""
    try:
        # 获取涨停跌停统计
        end_date = datetime.now().strftime('%Y%m%d')
        df = pro.limit_list(trade_date=end_date)
        
        if df is not None and len(df) > 0:
            limit_up = len(df[df['limit'] == 'U'])
            limit_down = len(df[df['limit'] == 'D'])
            return {'limit_up': limit_up, 'limit_down': limit_down}
    except:
        pass
    return None

def main():
    print("=" * 60)
    print("A股市场趋势分析")
    print("=" * 60)
    print()
    
    pro = get_tushare_pro()
    
    # 主要指数
    indices = [
        ('000001.SH', '上证指数'),
        ('399001.SZ', '深证成指'),
        ('399006.SZ', '创业板指'),
        ('000300.SH', '沪深300'),
        ('000905.SH', '中证500'),
    ]
    
    print("【主要指数表现】")
    print("-" * 60)
    print(f"{'指数名称':<12} {'最新':<10} {'5日':<8} {'10日':<8} {'20日':<8}")
    print("-" * 60)
    
    for code, name in indices:
        trend = get_index_trend(pro, code, name)
        if trend:
            print(f"{trend['name']:<12} {trend['latest']:<10.2f} "
                  f"{trend['change_5d']:+7.2f}% {trend['change_10d']:+7.2f}% "
                  f"{trend['change_20d']:+7.2f}%")
    
    print()
    
    # 市场情绪
    sentiment = get_market_sentiment(pro)
    if sentiment:
        print("【市场情绪】")
        print("-" * 60)
        print(f"涨停家数: {sentiment['limit_up']}")
        print(f"跌停家数: {sentiment['limit_down']}")
        print(f"涨跌比: {sentiment['limit_up']/(sentiment['limit_down']+1):.1f}:1")
    
    print()
    print("=" * 60)
    print("数据更新时间:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 60)

if __name__ == '__main__':
    main()
