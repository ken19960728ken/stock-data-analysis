# Stock Data Analysis

股市 K 線資料分析工具，分析股票創歷史新高（ATH）及 Rolling Window 新高後的行為模式。

## 分析內容

- 每次創高後，多久才達到下一個新高（山峰間距）
- 創高後多快開始下跌
- 創高後到下一次新高之間的最大回撤幅度

## 使用方式

```bash
# 安裝依賴
uv sync

# 啟動 Jupyter Notebook
uv run jupyter notebook
```

開啟 `notebooks/01_peak_analysis.ipynb`，修改 `TICKER` 變數即可分析不同標的（如 `SPY`、`2330.TW`、`AAPL`）。

## Tech Stack

- Python 3.13 + uv
- yfinance（歷史資料）
- pandas / numpy（資料處理）
- matplotlib / mplfinance（視覺化）