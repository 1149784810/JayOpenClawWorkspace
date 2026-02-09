# Tushare Stock Data Skill

## Description

Access Chinese A-share stock market data through Tushare API. Provides stock basics, market trends, sector analysis, and technical indicators.

## Requirements

- Python 3.8+
- tushare package (`pip install tushare`)
- Tushare API token (free registration at tushare.pro)

## Quick Start

### 1. Get API Token
Visit https://tushare.pro/register to register and get your free API token.

### 2. Configure Token

**Option A - Environment Variable:**
```powershell
$env:TUSHARE_TOKEN="your_token_here"
```

**Option B - Config File:**
Create `~/.tushare/config.json`:
```json
{"token": "your_token_here"}
```

### 3. Install Dependency
```bash
pip install tushare
```

## Scripts

### Sector Analysis (板块分析)
```bash
python scripts/sector_analysis.py
```
Analyzes industry and concept sectors with recent performance trends.

### Market Trend (市场趋势)
```bash
python scripts/market_trend.py
```
Shows major index performance and market sentiment.

### Stock Basics (股票基本信息)
```bash
python scripts/stock_basic.py
```
Lists all listed stocks and basic market statistics.

### Sina Data (新浪财经 - 无需Token)
```bash
python scripts/sina_sectors.py
```
Basic sector data from Sina Finance (no API key required).

## Troubleshooting

### SSL Error during pip install
If you see SSL errors, try:
```bash
pip install tushare --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

### No module named 'tushare'
Ensure pip and python are from the same environment:
```bash
python -m pip install tushare
```

## API Reference

Full API documentation: https://tushare.pro/document/2

## Data Sources

- **Tushare Pro**: Real-time A-share data (requires token)
- **Sina Finance**: Basic market data (no token required)
