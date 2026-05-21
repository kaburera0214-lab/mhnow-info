"""
fetch_news.py — モンハンNow 公式ニュース取得スクリプト
GitHub Actions から定期実行されて news.json に保存する
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
import time
from datetime import datetime, timezone

URL    = 'https://monsterhunternow.com/ja/news'
BASE   = 'https://monsterhunternow.com'
OUTPUT = 'news.json'
MAX_ITEMS = 20

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
}

# ── 記事詳細から本文を抽出 ────────────────────────────
def fetch_article_body(url, max_chars=280):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        # ナビ・ヘッダー・フッターを除去
        for tag in soup.find_all(['nav', 'header', 'footer', 'script', 'style']):
            tag.decompose()

        # 本文コンテナを探す（複数セレクタを順番に試す）
        body = None
        for sel in ['article', 'main', '[class*="content"]', '[class*="article"]', '[class*="post"]']:
            body = soup.select_one(sel)
            if body:
                break
        if not body:
            body = soup.body

        # p タグからテキストを収集（10文字以下の断片は除外）
        texts = [
            ' '.join(p.get_text().split())
            for p in (body or soup).find_all('p')
            if len(p.get_text(strip=True)) > 10
        ]
        full = ' '.join(texts)
        if not full:
            return ''
        return (full[:max_chars] + '…') if len(full) > max_chars else full
    except Exception as e:
        print(f'  スキップ ({e}): {url}')
        return ''

# ── 取得 ──────────────────────────────────────────────
print(f'取得中: {URL}')
try:
    res = requests.get(URL, headers=HEADERS, timeout=15)
    res.raise_for_status()
    res.encoding = 'utf-8'
except Exception as e:
    print(f'[ERROR] 取得失敗: {e}', file=sys.stderr)
    sys.exit(1)

# ── パース ────────────────────────────────────────────
soup  = BeautifulSoup(res.text, 'html.parser')
items = []
seen  = set()

for link in soup.find_all('a', href=True):
    href = link['href']

    # /ja/news/スラッグ 形式のリンクだけ処理
    if not href.startswith('/ja/news/'):
        continue
    if href in ('/ja/news', '/ja/news/'):
        continue
    if href in seen:
        continue
    seen.add(href)

    # 最も近い意味のあるコンテナを探す
    container = (
        link.find_parent('li') or
        link.find_parent('article') or
        link.find_parent(class_=lambda c: c and any(
            k in ' '.join(c) for k in ['news', 'card', 'item', 'post']
        )) or
        link.find_parent('div') or
        link.parent
    )

    # タイトル（見出しタグを優先）
    title = ''
    for tag in ['h1', 'h2', 'h3', 'h4']:
        el = container.find(tag)
        if el:
            title = ' '.join(el.get_text().split())
            break
    if not title:
        title = ' '.join(link.get_text().split())
    if not title or len(title) < 4:
        continue

    # 概要
    p_el    = container.find('p')
    summary = ' '.join(p_el.get_text().split()) if p_el else ''

    # カテゴリ
    span_el  = container.find('span')
    category = ' '.join(span_el.get_text().split()) if span_el else 'お知らせ'
    if not category or len(category) > 20:
        category = 'お知らせ'

    # サムネイル画像
    img_el = container.find('img')
    image  = ''
    if img_el:
        image = img_el.get('src') or img_el.get('data-src') or ''

    items.append({
        'title':    title,
        'summary':  summary,
        'category': category,
        'image':    image,
        'url':      BASE + href,
    })

    if len(items) >= MAX_ITEMS:
        break

# ── 各記事の詳細本文を取得 ────────────────────────────
print(f'各記事の詳細を取得中（{len(items)} 件）...')
for i, item in enumerate(items):
    print(f'  [{i+1}/{len(items)}] {item["title"][:25]}...')
    item['body_summary'] = fetch_article_body(item['url'])
    time.sleep(0.8)  # サーバーへの負荷軽減

# ── 保存 ──────────────────────────────────────────────
if not items:
    print('[WARN] 記事が0件でした。ページ構造が変わった可能性があります。', file=sys.stderr)
    print('既存の news.json は上書きしません。')
    sys.exit(0)

now = datetime.now(timezone.utc)
output = {
    'updated': now.strftime('%Y-%m-%d %H:%M UTC'),
    'count':   len(items),
    'items':   items,
}

with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'✓ {len(items)} 件を {OUTPUT} に保存しました')
