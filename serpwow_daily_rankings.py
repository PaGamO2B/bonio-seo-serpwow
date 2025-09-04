import os
import sys
import time
from datetime import datetime, timezone, timedelta
import requests
import pandas as pd

EXCEL_PATH = os.environ.get("KEYWORDS_EXCEL_PATH", "活頁簿1.xlsx")
SHEET_NAME = os.environ.get("KEYWORDS_SHEET_NAME", None)
DOMAIN_FILTER = os.environ.get("TARGET_DOMAIN", "bonio.co")
API_ENDPOINT = "https://api.serpwow.com/live/search"
GL = "tw"
HL = "zh-tw"
DEVICE = "desktop"
NUM_RESULTS = 100
PAUSE_SECONDS = float(os.environ.get("SERPWOW_PAUSE_SECONDS", "1.2"))
OUTDIR = os.environ.get("OUTPUT_DIR", "output")

def load_keywords(xlsx_path: str, sheet_name=None):
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name)
    if isinstance(df, dict):
        df = list(df.values())[0]
    series = df.iloc[:, 0].dropna().astype(str).map(str.strip)
    seen = set()
    kws = []
    for k in series.tolist():
        if k and k not in seen:
            seen.add(k)
            kws.append(k)
    return kws

def query_serpwow(api_key: str, keyword: str):
    params = {
        "api_key": api_key,
        "q": keyword,
        "gl": GL,
        "hl": HL,
        "device": DEVICE,
        "search_type": "web",
        "num": NUM_RESULTS
    }
    resp = requests.get(API_ENDPOINT, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def extract_rank_for_domain(data: dict, domain: str):
    org = data.get("organic_results", [])
    for idx, item in enumerate(org, start=1):
        link = item.get("link", "") or ""
        if domain in link:
            return idx, link
    return None, None

def main():
    api_key = os.environ.get("SERPWOW_API_KEY")
    if not api_key:
        print("ERROR: Missing SERPWOW_API_KEY in environment.", file=sys.stderr)
        sys.exit(2)

    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    datestamp = now.strftime("%Y%m%d")

    try:
        keywords = load_keywords(EXCEL_PATH, SHEET_NAME)
    except Exception as e:
        print(f"ERROR: failed to load keywords from {EXCEL_PATH}: {e}", file=sys.stderr)
        sys.exit(3)

    results = []
    for kw in keywords:
        try:
            data = query_serpwow(api_key, kw)
            rank, url = extract_rank_for_domain(data, DOMAIN_FILTER)
            results.append([kw, rank if rank is not None else "未上榜", url if url else "-", timestamp_str])
        except Exception as e:
            results.append([kw, "ERROR", str(e), timestamp_str])
        time.sleep(PAUSE_SECONDS)

    df = pd.DataFrame(results, columns=["Keyword", "Rank/Position", "URL shown", "Timestamp"])

    os.makedirs(OUTDIR, exist_ok=True)
    csv_path = os.path.join(OUTDIR, f"seo_rankings_{datestamp}.csv")
    xlsx_path = os.path.join(OUTDIR, f"seo_rankings_{datestamp}.xlsx")
    latest_csv = os.path.join(OUTDIR, "latest.csv")

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    try:
        df.to_excel(xlsx_path, index=False)
    except Exception as e:
        print(f"WARN: failed to write Excel: {e}", file=sys.stderr)

    df.to_csv(latest_csv, index=False, encoding="utf-8-sig")

    print(f"Wrote: {csv_path}")
    print(f"Wrote: {xlsx_path}")
    print(f"Wrote: {latest_csv}")

if __name__ == "__main__":
    main()
