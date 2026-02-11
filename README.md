# autotrade-v2 (Python 3.10 Skeleton)

此專案為交易系統骨架，僅建立基礎目錄與資料模型，**不包含 Alpaca 整合**，且**不實作 Entry/Exit 邏輯**。

## 專案結構

- `core/`
- `engines/`
- `adapters/`
- `state/`
- `scheduler/`
- `logger/`

## 已建立資料模型（dataclasses）

位於 `core/models.py`：

- `BarRow`
- `EntrySignal`
- `Blocked`
- `EntryDecision`
- `PositionSnapshot`
- `ExitSignal`
- `Skip`
- `ExitDecision`

## 環境需求

- Python 3.10+

## 安裝

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 執行

```bash
python main.py
```

成功時會顯示 skeleton 可執行訊息與一筆 `BarRow` 範例。
