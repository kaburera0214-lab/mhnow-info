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

# ── 記事詳細から構造化データを抽出 ──────────────────
def cut_at_sentence(text, max_len):
    """省略記号なし・文末で切る"""
    if len(text) <= max_len:
        return text
    cut = text.rfind('。', 0, max_len)
    return text[:cut + 1] if cut >= 0 else text[:max_len]

SHORT_HEADINGS = ['期間限定クエスト', 'プレミアムクエスト']
LIST_HEADINGS  = ['モンスター', '出現', '登場', '古龍種', '変異種', '亜種']

def make_section(heading, items):
    """items: list of (tag:'p'|'li', text:str, depth:int) → section dict"""
    is_monster = any(kw in heading for kw in LIST_HEADINGS)
    is_quest   = any(kw in heading for kw in SHORT_HEADINGS)

    # 重複除去
    seen, unique = set(), []
    for tag, text, depth in items:
        if text and text not in seen:
            seen.add(text)
            unique.append((tag, text, depth))
    if not unique:
        return None

    has_nested = any(d > 0 for _, _, d in unique)
    has_list   = any(t == 'li' for t, _, _ in unique)

    if is_monster:
        # モンスター名を1行ずつ（liのみ、なければ全項目）
        names = [txt for tag, txt, _ in unique if tag == 'li'] \
             or [txt for _, txt, _ in unique]
        body_text = '\n'.join(names)

    elif is_quest:
        flat = ' '.join(txt for _, txt, _ in unique)
        dots = [i for i, c in enumerate(flat) if c == '。']
        idx  = dots[1] if len(dots) > 1 else (dots[0] if dots else -1)
        body_text = flat[:idx + 1] if idx >= 0 else flat[:150]

    elif has_nested or has_list:
        # 階層構造を保持（親・子リスト）
        lines = [('　└ ' if d > 0 else '') + txt for _, txt, d in unique]
        body_text = '\n'.join(lines)

    else:
        flat = ' '.join(txt for _, txt, _ in unique)
        body_text = cut_at_sentence(flat, 400)

    return {'heading': heading, 'body': body_text} if body_text else None


def fetch_article_detail(url):
    result = {'date': '', 'teaser': '', 'sections': []}
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        # 日付
        date_meta = soup.find('meta', property='article:published_time')
        if date_meta and date_meta.get('content'):
            result['date'] = date_meta['content'][:10].replace('-', '/')
        else:
            time_el = soup.find('time')
            if time_el:
                result['date'] = (time_el.get('datetime','') or time_el.get_text())[:10].replace('-','/')

        # OGP teaser（100文字・文末カット）
        og = soup.find('meta', property='og:description') \
          or soup.find('meta', attrs={'name': 'description'})
        if og and og.get('content'):
            result['teaser'] = cut_at_sentence(og['content'].strip(), 100)

        # ノイズ除去
        for tag in soup.find_all(['nav', 'header', 'footer', 'script', 'style', 'noscript']):
            tag.decompose()

        body = soup.select_one('article, main, [class*="content"], [class*="article"]') \
            or soup.body
        if not body:
            return result

        sections        = []
        current_heading = ''
        current_items   = []   # (tag, text, depth)

        def flush():
            s = make_section(current_heading, current_items)
            if s:
                sections.append(s)
            current_items.clear()

        for el in body.find_all(['h2', 'h3', 'h4', 'p', 'li']):
            if el.name in ('h2', 'h3', 'h4'):
                flush()
                current_heading = ' '.join(el.get_text().split())
            elif el.name == 'p':
                t = ' '.join(el.get_text().split())
                if t and len(t) > 10:
                    current_items.append(('p', t, 0))
            elif el.name == 'li':
                # 子リストを一時除去して直接テキストだけ取得
                child_ul = el.find(['ul', 'ol'])
                if child_ul:
                    saved = child_ul.extract()
                    t = ' '.join(el.get_text().split())
                    el.append(saved)
                else:
                    t = ' '.join(el.get_text().split())
                if not t or len(t) < 3:
                    continue
                # ネスト深度（祖先liの数）
                depth, p = 0, el.parent
                while p and p != body:
                    if p.name == 'li':
                        depth += 1
                    p = p.parent
                current_items.append(('li', t, depth))

        flush()

        # 見出しなし
        if not sections:
            paras = [' '.join(p.get_text().split())
                     for p in body.find_all('p') if len(p.get_text(strip=True)) > 10]
            seen, uniq = set(), []
            for p in paras[:6]:
                if p not in seen:
                    seen.add(p); uniq.append(p)
            if uniq:
                sections = [{'heading': '', 'body': cut_at_sentence(' '.join(uniq), 400)}]

        result['sections'] = sections
    except Exception as e:
        print(f'  スキップ ({e}): {url}')
    return result

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
    detail = fetch_article_detail(item['url'])
    item['date']     = detail['date']
    item['teaser']   = detail['teaser']
    item['sections'] = detail['sections']
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
