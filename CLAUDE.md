# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

股市 K 線資料分析專案。使用 Python 抓取歷史 K 線資料，透過 Jupyter Notebook 進行視覺化分析。

## Tech Stack

- **Python 3.13** (uv 管理虛擬環境與套件)
- **yfinance** — 抓取股票歷史 K 線資料
- **pandas / numpy** — 資料處理與運算
- **matplotlib / mplfinance** — K 線圖與技術指標視覺化
- **Jupyter Notebook** — 互動式分析與呈現

## Commands

```bash
# 啟動 Jupyter Notebook
uv run jupyter notebook

# 執行 Python 腳本
uv run python <script.py>

# 新增套件
uv add <package>

# 重建環境
rm -rf .venv && uv sync
```

## Architecture

```
stock-data-analysis/
├── notebooks/       # Jupyter notebooks（分析與視覺化）
├── src/             # 可重用模組（資料抓取、指標計算、繪圖工具）
├── data/            # 快取的原始資料（.csv/.parquet）
├── pyproject.toml   # 專案設定與依賴
└── CLAUDE.md
```

## Conventions

- Notebook 命名格式：`{序號}_{主題}.ipynb`（如 `01_basic_candlestick.ipynb`）
- 資料抓取結果快取至 `data/` 避免重複 API 呼叫
- 技術指標計算抽成獨立函式放 `src/`，notebook 只負責呼叫與呈現
- 使用 mplfinance 繪製 K 線圖為首選，matplotlib 用於自訂圖表
