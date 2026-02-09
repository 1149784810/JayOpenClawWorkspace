# Tushare Skill

A skill for accessing Chinese stock market data via Tushare API.

## Installation

```bash
pip install tushare
```

## Setup

1. Get your Tushare token from https://tushare.pro
2. Set environment variable:
   ```bash
   export TUSHARE_TOKEN="your_token_here"
   ```

## Usage

```bash
# Get stock basic info
python scripts/stock_basic.py

# Get market trends
python scripts/market_trend.py

# Get sector performance
python scripts/sector_analysis.py
```

## Features

- Stock basic information
- Daily market data
- Sector/industry analysis
- Market trends
- Technical indicators
