import numpy as np
import pandas as pd


def _extract_summit_peaks(
    df: pd.DataFrame, is_peak_col: str, price_col: str
) -> list[int]:
    """從連續創高群組中取出每組的最高點位置（山峰頂點）。"""
    peak_mask = df[is_peak_col].values
    prices = df[price_col].values
    summits = []
    i = 0
    n = len(df)
    while i < n:
        if peak_mask[i]:
            group_best_pos = i
            group_best_price = prices[i]
            j = i + 1
            while j < n and peak_mask[j]:
                if prices[j] >= group_best_price:
                    group_best_pos = j
                    group_best_price = prices[j]
                j += 1
            summits.append(group_best_pos)
            i = j
        else:
            i += 1
    return summits


def _compute_metrics(
    df: pd.DataFrame, summit_positions: list[int], price_col: str
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """計算每個山峰的指標：到下一個山峰天數、開始下跌天數、最大回撤%。"""
    days_to_next = pd.Series(np.nan, index=df.index)
    days_to_decline = pd.Series(np.nan, index=df.index)
    max_drawdown_pct = pd.Series(np.nan, index=df.index)
    prices = df[price_col].values

    for k, pos in enumerate(summit_positions):
        next_pos = summit_positions[k + 1] if k < len(summit_positions) - 1 else len(df)
        days_to_next.iloc[pos] = next_pos - pos if k < len(summit_positions) - 1 else np.nan

        peak_price = prices[pos]
        between = prices[pos + 1:next_pos]

        if len(between) > 0:
            min_price = between.min()
            max_drawdown_pct.iloc[pos] = (min_price - peak_price) / peak_price * 100

            for future_pos in range(pos + 1, next_pos):
                if prices[future_pos] < peak_price:
                    days_to_decline.iloc[pos] = future_pos - pos
                    break

    return days_to_next, days_to_decline, max_drawdown_pct


def find_ath_peaks(df: pd.DataFrame, price_col: str = "Close") -> pd.DataFrame:
    result = df.copy()
    cummax = result[price_col].cummax()
    result["_is_ath_raw"] = result[price_col] >= cummax

    summits = _extract_summit_peaks(result, "_is_ath_raw", price_col)

    result["is_ath"] = False
    for pos in summits:
        result.iloc[pos, result.columns.get_loc("is_ath")] = True

    days_to_next, days_to_decline, drawdown = _compute_metrics(result, summits, price_col)
    result["days_to_next_ath"] = days_to_next
    result["days_to_decline"] = days_to_decline
    result["max_drawdown_pct"] = drawdown
    result.drop(columns=["_is_ath_raw"], inplace=True)
    return result


def find_rolling_peaks(
    df: pd.DataFrame, window: int = 252, price_col: str = "Close"
) -> pd.DataFrame:
    result = df.copy()
    rolling_max = result[price_col].rolling(window=window, min_periods=window).max()
    result["_is_rolling_raw"] = result[price_col] >= rolling_max

    summits = _extract_summit_peaks(result, "_is_rolling_raw", price_col)

    result["is_rolling_peak"] = False
    for pos in summits:
        result.iloc[pos, result.columns.get_loc("is_rolling_peak")] = True

    days_to_next, days_to_decline, drawdown = _compute_metrics(result, summits, price_col)
    result["days_to_next_rolling_peak"] = days_to_next
    result["days_to_decline_from_rolling"] = days_to_decline
    result["max_drawdown_pct_rolling"] = drawdown
    result.drop(columns=["_is_rolling_raw"], inplace=True)
    return result
