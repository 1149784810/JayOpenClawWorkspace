#!/usr/bin/env python3
"""
Tushare Stock Basic Information
获取股票基本信息
"""

import sys
import os
import json

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

def main():
    print("=" * 60)
    print("股票基本信息查询")
    print("=" * 60)
    print()
    
    pro = get_tushare_pro()
    
    try:
        # 获取股票列表
        df = pro.stock_basic(exchange='', list_status='L')
        
        print(f"【市场概况】")
        print(f"上市股票总数: {len(df)}")
        print()
        
        # 按交易所统计
        sh_count = len(df[df['exchange'] == 'SSE'])
        sz_count = len(df[df['exchange'] == 'SZSE'])
        bj_count = len(df[df['exchange'] == 'BSE'])
        
        print(f"上海证券交易所: {sh_count} 只")
        print(f"深圳证券交易所: {sz_count} 只")
        print(f"北京证券交易所: {bj_count} 只")
        print()
        
        # 显示最新上市的几只股票
        print("【最新上市股票】(前10只)")
        print("-" * 60)
        recent = df.sort_values('list_date', ascending=False).head(10)
        for _, row in recent.iterrows():
            print(f"{row['ts_code']:<12} {row['name']:<12} {row['list_date']:<12} {row['industry']}")
        
    except Exception as e:
        print(f"获取数据失败: {e}")
    
    print()
    print("=" * 60)

if __name__ == '__main__':
    main()
