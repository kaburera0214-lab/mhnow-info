"""
fetch_sns.py — YouTubeチャンネルから最新動画を取得して sns.json に保存
GitHub Actions から定期実行される
"""

import requests
import json
import os
import sys
from datetime import datetime, timezone

API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
OUTPUT  = 'sns.json'
MAX_PER_CHANNEL = 6   # 1チャンネルあたり最大取得数

# 対象チャンネル
CHANNELS = [
    {'id': 'UCFCgvaVNYdiZqAU56AraKjg', 'name': 'さーどら'},
    {'id': 'UCTykXxcnqEZpzyzs5-vknNA', 'name': '怠惰な人'},
    {'id': 'UCAmXPLf3OGaeZe-XTfF-WcQ', 'name': 'やぎなまず'},
]

BASE = 'https://www.googleapis.com/youtube/v3'

# タイトルから武器種を推定
WEAPONS = ['大剣','太刀','片手剣','双剣','ハンマー','狩猟笛','ランス',
           'ガンランス','スラッシュアックス','チャージアックス',
           '操虫棍','弓','ライトボウガン','ヘビィボウガン']

def extract_weapon(title):
    for w in WEAPONS:
        if w in title:
            return w
    return ''

def extract_context(title):
    ctx = []
    if '大量発生' in title:
        ctx.append('大量発生')
    if '拠点' in title or '要撃' in title:
        ctx.append('拠点要撃戦')
    return ctx

def fetch_channel(channel):
    ch_id   = channel['id']
    ch_name = channel['name']
    print(f'  取得中: {ch_name}')

    # ① 最新動画を検索（モンハンNow 関連）
    search_res = requests.get(f'{BASE}/search', params={
        'part':      'snippet',
        'channelId': ch_id,
        'q':         'モンハンNow OR モンハンNOW OR MHNow',
        'maxResults': MAX_PER_CHANNEL,
        'order':     'date',
        'type':      'video',
        'key':       API_KEY,
    }, timeout=10)
    search_res.raise_for_status()
    search_data = search_res.json()
    items = search_data.get('items', [])

    if not items:
        print(f'    → 動画なし')
        return [], 0

    video_ids = [it['id']['videoId'] for it in items]

    # ② 動画の再生数を取得
    stats_res = requests.get(f'{BASE}/videos', params={
        'part': 'statistics',
        'id':   ','.join(video_ids),
        'key':  API_KEY,
    }, timeout=10)
    stats_res.raise_for_status()
    stats_map = {
        it['id']: it['statistics']
        for it in stats_res.json().get('items', [])
    }

    # ③ チャンネル登録者数を取得
    ch_res = requests.get(f'{BASE}/channels', params={
        'part': 'statistics',
        'id':   ch_id,
        'key':  API_KEY,
    }, timeout=10)
    ch_res.raise_for_status()
    ch_items = ch_res.json().get('items', [])
    sub_count = int(ch_items[0]['statistics'].get('subscriberCount', 0)) if ch_items else 0

    results = []
    for it in items:
        vid_id  = it['id']['videoId']
        snippet = it['snippet']
        stats   = stats_map.get(vid_id, {})
        title   = snippet.get('title', '')

        results.append({
            'id':              vid_id,
            'title':           title,
            'source':          'YouTube',
            'author':          ch_name,
            'url':             f'https://www.youtube.com/watch?v={vid_id}',
            'youtubeId':       vid_id,
            'thumbnail':       snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
            'postedAt':        snippet.get('publishedAt', '')[:10],
            'viewCount':       int(stats.get('viewCount', 0)),
            'subscriberCount': sub_count,
            'weapon':          extract_weapon(title),
            'weaponElement':   '',
            'targetMonsters':  [],
            'context':         extract_context(title),
            'difficulty':      '',
            'armorSkills':     [],
            'notes':           '',
        })

    print(f'    → {len(results)} 件取得（登録者数: {sub_count:,}）')
    return results, sub_count


if not API_KEY:
    print('[ERROR] YOUTUBE_API_KEY が設定されていません', file=sys.stderr)
    sys.exit(1)

print('YouTube動画を取得中...')
all_items = []
for ch in CHANNELS:
    try:
        videos, _ = fetch_channel(ch)
        all_items.extend(videos)
    except Exception as e:
        print(f'  [WARN] {ch["name"]} 失敗: {e}')

if not all_items:
    print('[WARN] 動画が0件でした。sns.json は更新しません。')
    sys.exit(0)

now = datetime.now(timezone.utc)
output = {
    'updated': now.strftime('%Y-%m-%d %H:%M UTC'),
    'count':   len(all_items),
    'items':   all_items,
}

with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'✓ {len(all_items)} 件を {OUTPUT} に保存しました')
