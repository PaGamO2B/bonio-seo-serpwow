# Cloud Automation: SERP Wow → GitHub Actions → Output CSV/Excel

這個專案讓你不用開電腦，也能在雲端每天自動抓取 34 個關鍵字在 Taiwan / Desktop / bonio.co 的排名，並把結果存到 repo 的 `output/` 目錄。
你只需要把 `SERPWOW_API_KEY` 放進 GitHub Secrets，就能每天 **Asia/Taipei 09:30（UTC 01:30）** 自動更新。

## 快速部署
1. 在 GitHub 建一個 **公開或私有** 的新 repository（例如：`bonio-seo-serpwow`）。
2. 把下列檔案加到 repo 根目錄：
   - `serpwow_daily_rankings.py`
   - `requirements.txt`
   - `README_CLOUD.md`
   - `活頁簿1.xlsx`（第一欄放 34 個關鍵字，含「企業社會責任」）
   - `.github/workflows/serpwow.yml`
3. 到 GitHub → Repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**：
   - 名稱：`SERPWOW_API_KEY`
   - 值：你的 SERP Wow API Key
4. 推送後，GitHub Actions 會在 **每週一～五 01:30 UTC**（= **09:30 Asia/Taipei**）自動執行。
   - 你也可以在 Actions 頁面手動 **Run workflow** 做首次驗證。

## 產出
- `output/latest.csv`（永遠指向最新跑的結果）
- `output/seo_rankings_YYYYMMDD.csv`
- `output/seo_rankings_YYYYMMDD.xlsx`

## 給 ChatGPT 用（每日自動貼表格）
1. 讓 repo **公開**（或放在可提供 raw 檔案的地方）。
2. 取得 `latest.csv` 的 RAW 連結（例如：
   `https://raw.githubusercontent.com/<owner>/<repo>/main/output/latest.csv`）。
3. 回到這個對話，把 RAW 連結貼給我。  
   我會在平日 09:33 自動抓取 `latest.csv`，轉成 Markdown 表格貼回來。

> 如果你要私有 repo，也可以開啟 GitHub Pages 或把檔案同步到公開的雲端存放（我只需要一個能公開讀取的 URL）。
